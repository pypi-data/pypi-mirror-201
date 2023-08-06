from __future__ import annotations

import collections.abc
import time
import uuid
import warnings
from datetime import datetime, timezone
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)
from urllib.parse import urljoin

import pandas as pd
import requests
from pydantic import BaseModel, ValidationError
from requests import HTTPError
from requests import JSONDecodeError as RequestsJSONDecodeError
from requests.sessions import SessionRedirectMixin

from chalk._version import __version__ as chalkpy_version
from chalk.client import ChalkClient, OnlineQueryResult
from chalk.client.dataset import DatasetImpl, DatasetVersion, dataset_from_response, load_dataset
from chalk.client.exc import (
    ChalkAuthException,
    ChalkBaseException,
    ChalkComputeResolverException,
    ChalkDatasetDownloadException,
    ChalkOfflineQueryException,
    ChalkOnlineQueryException,
    ChalkRecomputeDatasetException,
    ChalkResolverRunException,
    ChalkUpdateResolverException,
    ChalkWhoAmIException,
)
from chalk.client.models import (
    ChalkError,
    ComputeResolverOutputRequest,
    ComputeResolverOutputResponse,
    CreateOfflineQueryJobRequest,
    CreateOfflineQueryJobResponse,
    DatasetRecomputeRequest,
    DatasetResponse,
    DatasetRevisionResponse,
    ErrorCode,
    ExchangeCredentialsRequest,
    ExchangeCredentialsResponse,
    FeatureResult,
    GetOfflineQueryJobResponse,
    OfflineQueryContext,
    OfflineQueryInput,
    OnlineQueryContext,
    OnlineQueryRequest,
    OnlineQueryResponse,
    ResolverRunResponse,
    TriggerResolverRunRequest,
    UpdateResolverResponse,
    WhoAmIResponse,
)
from chalk.config.auth_config import load_token
from chalk.features import DataFrame, Feature, FeatureNotFoundException, ensure_feature
from chalk.features._encoding.inputs import recursive_encode
from chalk.features.pseudofeatures import CHALK_TS_FEATURE
from chalk.features.tag import BranchId, EnvironmentId
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl

_logger = get_logger(__name__)

T = TypeVar("T")


class _ChalkClientConfig(BaseModel):
    name: str
    client_id: str
    client_secret: str
    api_server: str
    active_environment: Optional[str]
    branch: Optional[BranchId]


def _to_offline_query_input(
    input: Union[Mapping[Union[str, Feature, Any], Any], pd.DataFrame, pl.DataFrame, DataFrame],
    input_times: Sequence[datetime] | datetime | None,
) -> OfflineQueryInput:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if isinstance(input, (DataFrame, pl.DataFrame)):
        input = input.to_pandas()
    if isinstance(input, collections.abc.Mapping):
        input = {str(k): v for (k, v) in input.items()}
    pd_dataframe: pd.DataFrame
    if isinstance(input, pd.DataFrame):
        pd_dataframe = input
    else:
        pd_dataframe = pd.DataFrame(input)

    columns = pd_dataframe.columns
    matrix: List[List[Any]] = pd_dataframe.T.values.tolist()

    columns_fqn = [str(c) for c in (*columns, CHALK_TS_FEATURE)]
    if input_times is None:
        input_times = datetime.now(timezone.utc)
    if isinstance(input_times, datetime):
        input_times = [input_times for _ in range(len(pd_dataframe))]
    local_tz = datetime.now(timezone.utc).astimezone().tzinfo

    input_times = [x.replace(tzinfo=local_tz) if x.tzinfo is None else x for x in input_times]
    input_times = [x.astimezone(timezone.utc) for x in input_times]

    matrix.append([a for a in input_times])

    for col_index, column in enumerate(matrix):
        for row_index, value in enumerate(column):
            try:
                f = Feature.from_root_fqn(columns_fqn[col_index])
            except FeatureNotFoundException:
                # The feature is not in the graph, so passing the value as-is and hoping it's possible
                # to json-serialize it
                encoded_feature = value
            else:
                encoded_feature = f.converter.from_rich_to_json(
                    value,
                    missing_value_strategy="error",
                )

            matrix[col_index][row_index] = encoded_feature

    return OfflineQueryInput(
        columns=columns_fqn,
        values=matrix,
    )


class OnlineQueryResponseImpl(OnlineQueryResult):
    data: List[FeatureResult]
    errors: List[ChalkError]
    warnings: List[str]

    def __init__(
        self,
        data: List[FeatureResult],
        errors: List[ChalkError],
        warnings: List[str],
    ):
        self.data = data
        self.errors = errors
        self.warnings = warnings
        for d in self.data:
            if d.value is not None:
                try:
                    f = Feature.from_root_fqn(d.field)
                except FeatureNotFoundException:
                    self.warnings.append(
                        f"Return data {d.field}:{d.value} cannot be decoded. Attempting to JSON decode"
                    )
                else:
                    d.value = f.converter.from_json_to_rich(d.value)

        self._values = {d.field: d for d in self.data}

    def _df_repr(self):
        if self.errors:
            info = [vars(x) for x in self.errors]
        else:
            info = [{"field": x.field, "value": x.value, "error": x.error, "ts": x.ts} for x in self.data]
        return pd.DataFrame(info)

    def __repr__(self) -> str:
        return repr(self._df_repr())

    def _repr_html_(self) -> Union[str, None]:
        return self._df_repr()._repr_html_()

    def get_feature(self, feature: Any) -> Optional[FeatureResult]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        return self._values.get(str(feature))

    def get_feature_value(self, feature: Any) -> Optional[Any]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        v = self.get_feature(feature)
        return v and v.value


class ChalkAPIClientImpl(ChalkClient):
    __name__ = "ChalkClient"
    __qualname__ = "chalk.client.ChalkClient"

    _latest_client: Optional[ChalkAPIClientImpl]

    def __repr__(self):
        return f"chalk.client.ChalkClient<{self._config.name}>"

    def __new__(cls, *args: Any, **kwargs: Any) -> ChalkClient:
        obj = object.__new__(ChalkAPIClientImpl)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
        api_server: Optional[str] = None,
        branch: Optional[BranchId] = None,
        _skip_cache: bool = False,
        session: Optional[requests.Session] = None,
    ):
        self.session: requests.Session = session or requests.Session()
        token = load_token(
            client_id=client_id,
            client_secret=client_secret,
            active_environment=environment,
            api_server=api_server,
            skip_cache=_skip_cache,
        )
        if token is None:
            raise ChalkAuthException()

        self._config = _ChalkClientConfig(
            name=token.name or "",
            client_id=token.clientId,
            client_secret=token.clientSecret,
            api_server=token.apiServer or "https://api.chalk.ai",
            branch=branch,
            active_environment=token.activeEnvironment,
        )

        self._default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"chalkpy-{chalkpy_version}",
            "X-Chalk-Client-Id": self._config.client_id,
            "X-Chalk-Features-Versioned": "true",
        }
        self._exchanged_credentials = False
        self._primary_environment = None

        self.__class__._latest_client = self

    def _exchange_credentials(self):
        _logger.debug("Performing a credentials exchange")
        resp = self.session.post(
            url=urljoin(self._config.api_server, f"v1/oauth/token"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=ExchangeCredentialsRequest(
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
                grant_type="client_credentials",
            ).dict(),
            timeout=10,
        )
        resp.raise_for_status()
        response_json = resp.json()
        try:
            creds = ExchangeCredentialsResponse(**response_json)
        except ValidationError:
            raise HTTPError(response=resp)
        self._default_headers["Authorization"] = f"Bearer {creds.access_token}"
        self._primary_environment = creds.primary_environment
        self._exchanged_credentials = True

    def _get_headers(
        self,
        environment_override: Optional[str],
        preview_deployment_id: Optional[str],
        branch: Optional[BranchId],
    ) -> dict[str, str]:
        x_chalk_env_id = environment_override or self._config.active_environment or self._primary_environment
        headers = dict(self._default_headers)  # shallow copy
        if x_chalk_env_id is not None:
            headers["X-Chalk-Env-Id"] = x_chalk_env_id
        if preview_deployment_id is not None:
            headers["X-Chalk-Preview-Deployment"] = preview_deployment_id
        if branch is not None:
            headers["X-Chalk-Branch-Id"] = branch
        elif self._config.branch is not None:
            headers["X-Chalk-Branch-Id"] = self._config.branch

        return headers

    @staticmethod
    def _raise_if_200_with_errors(response: BaseModel, exception_cls: Type[ChalkBaseException]):
        errors = getattr(response, "errors", None)
        if errors and isinstance(errors, list) and all(isinstance(e, ChalkError) for e in errors):
            errors = cast(List[ChalkError], errors)
            raise exception_cls(errors=errors)

    @staticmethod
    def _raise_http_error(http_error: HTTPError, exception_cls: Type[ChalkBaseException], **exception_kwargs: Any):
        detail = None
        try:
            response_json = http_error.response.json()
            if isinstance(response_json, Mapping):
                detail = response_json.get("detail")
        except RequestsJSONDecodeError:
            pass

        status_code = http_error.response.status_code
        known_error_code = None
        if status_code == 401:
            known_error_code = ErrorCode.UNAUTHENTICATED
        elif status_code == 403:
            known_error_code = ErrorCode.UNAUTHORIZED

        chalk_error = ChalkError(
            code=known_error_code or ErrorCode.INTERNAL_SERVER_ERROR,
            message=detail or f"Unexpected Chalk server error with status code {status_code}",
        )
        raise exception_cls(errors=[chalk_error], **exception_kwargs)

    def _request(
        self,
        method: str,
        uri: str,
        response: Type[T],
        json: Optional[BaseModel],
        environment_override: Optional[str],
        exception_cls: Type[ChalkBaseException],
        preview_deployment_id: Optional[str],
        branch: Optional[BranchId],
        data: Optional[bytes] = None,
        **exception_kwargs: Any,
    ) -> T:
        # Track whether we already exchanged credentials for this request
        exchanged_credentials = False
        if not self._exchanged_credentials:
            exchanged_credentials = True
            try:
                self._exchange_credentials()
            except HTTPError as e:
                self._raise_http_error(http_error=e, exception_cls=exception_cls, **exception_kwargs)
        headers = self._get_headers(
            environment_override=environment_override,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        url = urljoin(self._config.api_server, uri)
        json_body = json and json.dict()
        r = self.session.request(method=method, headers=headers, url=url, json=json_body, data=data)
        if r.status_code in (401, 403) and not exchanged_credentials:
            # It is possible that credentials expired, or that we changed permissions since we last
            # got a token. Exchange them and try again
            self._exchange_credentials()
            r = self.session.request(method=method, headers=headers, url=url, json=json_body, data=data)

        try:
            r.raise_for_status()
        except HTTPError as e:
            self._raise_http_error(http_error=e, exception_cls=exception_cls, **exception_kwargs)

        return response(**r.json())

    def whoami(self) -> WhoAmIResponse:
        return self._request(
            method="GET",
            uri=f"/v1/who-am-i",
            response=WhoAmIResponse,
            json=None,
            environment_override=None,
            exception_cls=ChalkWhoAmIException,
            preview_deployment_id=None,
            branch=None,
        )

    def upload_features(
        self,
        input: Mapping[Union[str, Feature, Any], Any],
        branch: Optional[BranchId] = None,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> Optional[List[ChalkError]]:
        return self.query(
            input=input,
            output=list(input.keys()),
            staleness=None,
            environment=environment,
            preview_deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        ).errors

    def query(
        self,
        input: Mapping[Union[str, Feature, Any], Any],
        output: Sequence[Union[str, Feature, Any]],
        staleness: Optional[Mapping[Union[str, Feature, Any], str]] = None,
        context: Optional[OnlineQueryContext] = None,  # Deprecated.
        environment: Optional[EnvironmentId] = None,
        tags: Optional[List[str]] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> OnlineQueryResponseImpl:
        environment = environment or (context and context.environment)
        tags = tags or (context and context.tags)
        encoded_inputs, encoding_warnings = recursive_encode(input)

        outputs: List[str] = [str(feature) for feature in output]

        request = OnlineQueryRequest(
            inputs=encoded_inputs,
            outputs=outputs,
            staleness={} if staleness is None else {ensure_feature(k).root_fqn: v for k, v in staleness.items()},
            context=OnlineQueryContext(
                environment=environment,
                tags=tags,
            ),
            deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        )

        resp = self._request(
            method="POST",
            uri="/v1/query/online",
            json=request,
            response=OnlineQueryResponse,
            environment_override=environment,
            exception_cls=ChalkOnlineQueryException,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        return OnlineQueryResponseImpl(data=resp.data, errors=resp.errors or [], warnings=encoding_warnings)

    def offline_query(
        self,
        input: Optional[Union[Mapping[Union[str, Feature, Any], Any], pd.DataFrame, pl.DataFrame, DataFrame]] = None,
        input_times: Union[Sequence[datetime], datetime, None] = None,
        output: Sequence[Union[str, Feature, Any]] = (),
        required_output: Sequence[Union[str, Feature, Any]] = (),
        environment: Optional[EnvironmentId] = None,
        dataset_name: Optional[str] = None,
        branch: Optional[BranchId] = None,
        max_samples: Optional[int] = None,
    ) -> DatasetImpl:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        del pl  # unused

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")
        optional_output_root_fqns = [str(f) for f in output]
        required_output_root_fqns = [str(f) for f in required_output]

        if input is None:
            query_input = None
        else:
            query_input = _to_offline_query_input(input, input_times)

        response = self._create_dataset_job(
            optional_output=optional_output_root_fqns,
            required_output=required_output_root_fqns,
            query_input=query_input,
            dataset_name=dataset_name,
            branch=branch,
            context=OfflineQueryContext(environment=environment),
            max_samples=max_samples,
        )
        return dataset_from_response(response, self)

    def get_training_dataframe(
        self,
        input: Union[
            Mapping[Union[str, Feature], Sequence[Any]],
            pd.DataFrame,
            pl.DataFrame,
            DataFrame,
        ],
        input_times: Union[Sequence[datetime], datetime, None] = None,
        output: Sequence[Union[str, Feature, Any]] = (),
        required_output: Sequence[Union[str, Feature, Any]] = (),
        output_ts: bool = False,
        context: Optional[OfflineQueryContext] = None,
        dataset: Optional[str] = None,
        max_samples: Optional[int] = None,
    ) -> pd.DataFrame:
        warnings.warn(
            DeprecationWarning("Method get_training_dataframe is deprecated. Please consider `.offline_query` instead.")
        )
        if context is None:
            context = OfflineQueryContext()
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        if isinstance(input, (DataFrame, pl.DataFrame)):
            input = input.to_pandas()

        if isinstance(input, collections.abc.Mapping):
            input = {str(k): v for (k, v) in input.items()}

        if not isinstance(input, pd.DataFrame):
            input = pd.DataFrame(input)

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")

        query_input = _to_offline_query_input(input, input_times)

        response = self._create_and_await_offline_query_job(
            optional_output=[str(x) for x in output],
            required_output=[str(x) for x in required_output],
            query_input=query_input,
            output_id=False,
            output_ts=output_ts,
            dataset_name=dataset,
            branch=None,
            context=context,
            max_samples=max_samples,
            preview_deployment_id=None,
            lazy=False,
        )
        if isinstance(response, pl.LazyFrame):
            response = response.collect()
        return response.to_pandas()

    def sample(
        self,
        output: Sequence[Union[str, Feature, Any]] = (),
        required_output: Sequence[Union[str, Feature, Any]] = (),
        output_id: bool = False,
        output_ts: bool = False,
        max_samples: Optional[int] = None,
        dataset: Optional[str] = None,
        branch: Optional[BranchId] = None,
        environment: Optional[EnvironmentId] = None,
    ) -> pd.DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        context = OfflineQueryContext(environment=environment)
        optional_output_root_fqns = [str(f) for f in output]
        required_output_root_fqns = [str(f) for f in required_output]

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")

        response = self._create_and_await_offline_query_job(
            query_input=None,
            optional_output=optional_output_root_fqns,
            required_output=required_output_root_fqns,
            max_samples=max_samples,
            context=context,
            output_id=output_id,
            output_ts=output_ts,
            dataset_name=dataset,
            branch=branch,
            preview_deployment_id=None,
            lazy=False,
        )
        if isinstance(response, pl.LazyFrame):
            response = response.collect()

        return response.to_pandas()

    def get_dataset(
        self,
        dataset_name: str,
        environment: Optional[EnvironmentId] = None,
    ) -> DatasetImpl:
        response: DatasetResponse = self._get_dataset(
            dataset_name=dataset_name,
            environment=environment,
        )
        if response.errors:
            raise ChalkDatasetDownloadException(
                dataset_name=dataset_name,
                errors=response.errors,
            )
        return dataset_from_response(response, self)

    def trigger_resolver_run(
        self,
        resolver_fqn: str,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = None,
    ) -> ResolverRunResponse:
        _logger.debug(f"Triggering resolver {resolver_fqn} to run")
        return self._request(
            method="POST",
            uri="/v1/runs/trigger",
            json=TriggerResolverRunRequest(resolver_fqn=resolver_fqn),
            response=ResolverRunResponse,
            environment_override=environment,
            exception_cls=ChalkResolverRunException,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )

    def get_run_status(
        self,
        run_id: str,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = None,
    ) -> ResolverRunResponse:
        response = self._request(
            method="GET",
            uri=f"/v1/runs/{run_id}",
            response=ResolverRunResponse,
            json=None,
            environment_override=environment,
            exception_cls=ChalkResolverRunException,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )

        return response

    def _create_and_await_offline_query_job(
        self,
        optional_output: List[str],
        required_output: List[str],
        query_input: Optional[OfflineQueryInput],
        max_samples: Optional[int],
        dataset_name: Optional[str],
        branch: Optional[BranchId],
        context: OfflineQueryContext,
        output_id: bool,
        output_ts: bool,
        preview_deployment_id: Optional[str],
        lazy: bool = True,
    ) -> Union[pl.DataFrame, pl.LazyFrame]:
        req = CreateOfflineQueryJobRequest(
            output=optional_output,
            required_output=required_output,
            destination_format="PARQUET",
            input=query_input,
            max_samples=max_samples,
            dataset_name=dataset_name,
            branch=branch,
        )
        response = self._create_offline_query_job(
            request=req,
            context=context,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        self._raise_if_200_with_errors(response=response, exception_cls=ChalkOfflineQueryException)
        return self._await_offline_query_job(
            job_id=response.job_id,
            outputs=[*optional_output, *required_output],
            lazy=lazy,
            context=context,
            output_id=output_id,
            output_ts=output_ts,
        )

    @overload
    def _await_offline_query_job(
        self,
        job_id: uuid.UUID,
        outputs: List[str],
        lazy: bool,
        context: Optional[OfflineQueryContext],
        output_id: bool,
        output_ts: bool,
        urls_only: Literal[False] = ...,
    ) -> Union[pl.DataFrame, pl.LazyFrame]:
        ...

    @overload
    def _await_offline_query_job(
        self,
        job_id: uuid.UUID,
        outputs: List[str],
        lazy: bool,
        context: Optional[OfflineQueryContext],
        output_id: bool,
        output_ts: bool,
        urls_only: Literal[True],
        branch: Optional[BranchId],
    ) -> List[str]:
        ...

    def _await_offline_query_job(
        self,
        job_id: uuid.UUID,
        outputs: List[str],
        lazy: bool,
        context: Optional[OfflineQueryContext],
        output_id: bool,
        output_ts: bool,
        urls_only: bool = False,
        branch: Optional[BranchId] = None,
    ) -> Union[pl.DataFrame, pl.LazyFrame, List[str]]:
        while True:
            status = self._get_job_status(job_id=job_id, environment=context and context.environment, branch=branch)
            if status.is_finished:
                break
            time.sleep(0.5)
        if urls_only:
            return status.urls
        return load_dataset(
            uris=status.urls,
            output_features=outputs,
            version=DatasetVersion(status.version),
            output_id=output_id,
            output_ts=output_ts,
            columns=status.columns,
            lazy=lazy,
        )

    def _recompute_dataset(
        self,
        dataset_name: str | None,
        dataset_id: uuid.UUID | None,
        revision_id: uuid.UUID | None,
        features: List[Union[str, Any]],
        branch: BranchId,
        environment: Optional[EnvironmentId],
    ) -> DatasetRevisionResponse:
        request = DatasetRecomputeRequest(
            dataset_name=dataset_name,
            dataset_id=str(dataset_id) if dataset_id is not None else None,
            revision_id=str(revision_id) if revision_id is not None else None,
            features=features,
            branch=branch,
        )
        return self._request(
            method="POST",
            uri="/v1/dataset/recompute",
            json=request,
            response=DatasetRevisionResponse,
            environment_override=environment,
            exception_cls=ChalkRecomputeDatasetException,
            preview_deployment_id=None,
            branch=branch,
            dataset_name=str(dataset_id),
        )

    def _create_dataset_job(
        self,
        optional_output: List[str],
        required_output: List[str],
        query_input: Optional[OfflineQueryInput],
        max_samples: Optional[int],
        dataset_name: Optional[str],
        branch: Optional[BranchId],
        context: OfflineQueryContext,
    ) -> DatasetResponse:
        req = CreateOfflineQueryJobRequest(
            output=optional_output,
            required_output=required_output,
            destination_format="PARQUET",
            input=query_input,
            max_samples=max_samples,
            dataset_name=dataset_name,
            branch=branch,
        )
        response = self._create_dataset_request(
            request=req,
            context=context,
            preview_deployment_id=None,
            branch=branch,
        )
        self._raise_if_200_with_errors(response=response, exception_cls=ChalkOfflineQueryException)
        return response

    def compute_resolver_output(
        self,
        input: Union[Mapping[Union[str, Feature], Any], pl.DataFrame, pd.DataFrame, DataFrame],
        input_times: List[datetime],
        resolver: str,
        context: Optional[OfflineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = None,
    ) -> pl.DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        if context is None:
            context = OfflineQueryContext()
        query_input = _to_offline_query_input(input, input_times)
        request = ComputeResolverOutputRequest(input=query_input, resolver_fqn=resolver)
        response = self._request(
            method="POST",
            uri="/v1/compute_resolver_output",
            json=request,
            response=ComputeResolverOutputResponse,
            environment_override=context.environment,
            exception_cls=ChalkComputeResolverException,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        self._raise_if_200_with_errors(response=response, exception_cls=ChalkComputeResolverException)

        while True:
            status = self._get_compute_job_status(
                job_id=response.job_id,
                context=context,
                preview_deployment_id=preview_deployment_id,
                branch=branch,
            )
            if status.is_finished:
                break
            time.sleep(0.5)

        df = load_dataset(
            uris=status.urls,
            version=status.version,
            executor=None,
            columns=status.columns,
        )
        if isinstance(df, pl.LazyFrame):
            df = df.collect()
        return df

    def _get_compute_job_status(
        self,
        job_id: str,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
        branch: Optional[BranchId] = None,
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v1/compute_resolver_output/{job_id}",
            response=GetOfflineQueryJobResponse,
            json=None,
            environment_override=context.environment,
            exception_cls=ChalkComputeResolverException,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )

    def _create_dataset_request(
        self,
        request: CreateOfflineQueryJobRequest,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
        branch: Optional[BranchId] = None,
    ):
        response = self._request(
            method="POST",
            uri="/v3/offline_query",
            json=request,
            response=DatasetResponse,
            environment_override=context.environment,
            exception_cls=ChalkOfflineQueryException,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        return response

    def _create_offline_query_job(
        self,
        request: CreateOfflineQueryJobRequest,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
        branch: Optional[BranchId] = None,
    ):
        response = self._request(
            method="POST",
            uri="/v2/offline_query",
            json=request,
            response=CreateOfflineQueryJobResponse,
            environment_override=context.environment,
            exception_cls=ChalkOfflineQueryException,
            preview_deployment_id=preview_deployment_id,
            branch=branch,
        )
        return response

    def _get_job_status(
        self, job_id: uuid.UUID, environment: Optional[EnvironmentId], branch: Optional[BranchId]
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v2/offline_query/{job_id}",
            response=GetOfflineQueryJobResponse,
            environment_override=environment,
            json=None,
            exception_cls=ChalkOfflineQueryException,
            preview_deployment_id=None,
            branch=branch,
        )

    def _get_dataset(self, dataset_name: str, environment: Optional[EnvironmentId]) -> DatasetResponse:
        return self._request(
            method="GET",
            uri=f"/v3/offline_query/{dataset_name}",
            response=DatasetResponse,
            environment_override=environment,
            json=None,
            exception_cls=ChalkDatasetDownloadException,
            dataset_name=dataset_name,
            preview_deployment_id=None,
            branch=None,
        )

    def _send_updated_resolver(
        self, environment: Optional[EnvironmentId], pickled_resolver: bytes
    ) -> UpdateResolverResponse:
        return self._request(
            method="POST",
            uri=f"/v1/update_resolver",
            response=UpdateResolverResponse,
            json=None,
            data=pickled_resolver,
            environment_override=environment,
            exception_cls=ChalkUpdateResolverException,
            preview_deployment_id=None,
            branch=None,
        )
