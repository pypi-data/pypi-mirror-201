from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Protocol, Sequence, Union, overload

import pandas as pd
import requests
from typing_extensions import TypeAlias

from chalk.client.exc import (
    ChalkAuthException,
    ChalkBaseException,
    ChalkDatasetDownloadException,
    ChalkOfflineQueryException,
    ChalkResolverRunException,
)
from chalk.client.models import (
    ChalkError,
    ChalkException,
    DatasetFilter,
    ErrorCode,
    ErrorCodeCategory,
    FeatureResult,
    OfflineQueryContext,
    OnlineQueryContext,
    OnlineQueryResponse,
    QueryStatus,
    ResolverRunResponse,
    WhoAmIResponse,
)
from chalk.features import DataFrame, Feature
from chalk.features.tag import BranchId, EnvironmentId

if TYPE_CHECKING:
    import polars as pl


class DatasetRevision(Protocol):
    """Class wrapper around revisions for Datasets."""

    revision_id: uuid.UUID
    """UUID for the revision job."""

    creator_id: str
    """UUID for the creator of the job."""

    outputs: List[str]
    """Output features for the dataset revision."""

    givens_uri: str | None
    """Location of the givens stored for the dataset."""

    status: QueryStatus
    """Status of the revision job."""

    filters: DatasetFilter
    """Filters performed on the dataset."""

    num_partitions: int
    """Number of partitions for revision job."""

    output_uris: str
    """Location of the outputs stored fo the dataset."""

    output_version: int
    """Storage version of the outputs."""

    num_bytes: Optional[int] = None
    """Number of bytes of the output, updated upon success."""

    created_at: Optional[datetime] = None
    """Timestamp for creation of revision job."""

    started_at: Optional[datetime] = None
    """Timestamp for start of revision job."""

    terminated_at: Optional[datetime] = None
    """Timestamp for end of revision job."""

    dataset_name: Optional[str] = None
    """Name of revision, if given."""

    dataset_id: Optional[uuid.UUID] = None
    """ID of revision, if name is given."""

    def get_data_as_polars(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pl.LazyFrame:
        """Loads a `pl.LazyFrame` containing the output.

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pl.LazyFrame`.
        output_ts
            Whether to return the timestamp feature in a column
            named `__chalk__.CHALK_TS` in the resulting `pl.LazyFrame`.

        Returns
        -------
        pl.LazyFrame
            a `pl.LazyFrame` materializing query output data.
        """
        ...

    def get_data_as_pandas(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pd.DataFrame:
        """Loads a `pd.DataFrame` containing the output.

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pd.DataFrame`.
        output_ts
            Whether to return the timestamp feature in a column
            named `__chalk__.CHALK_TS` in the resulting `pd.DataFrame`.

        Returns
        -------
        pd.DataFrame
            a `pd.DataFrame` materializing query output data.
        """
        ...

    def get_data_as_dataframe(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> DataFrame:
        """Loads a Chalk `DataFrame` containing the output.


        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `DataFrame`.
        output_ts
            Whether to return the timestamp feature in a column
            named `__chalk__.CHALK_TS` in the resulting `DataFrame`.

        Returns
        -------
        DataFrame
            a `DataFrame` materializing query output data.
        """
        ...

    def download_data(
        self,
        path: str,
        output_id: bool = False,
        output_ts: bool = False,
        num_executors: Optional[int] = None,
    ) -> None:
        """Downloads output files pertaining to the revision to given path.

        Datasets are stored in Chalk as sharded Parquet files. With this
        method, you can download those raw files into a directory for processing
        with other tools.

        Parameters
        ----------
        path
            A directory where the Parquet files from the dataset will be downloaded.

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `DataFrame`.
        output_ts
            Whether to return the timestamp feature in a column
            named `__chalk__.CHALK_TS` in the resulting `DataFrame`.
        num_executors
            Number of executors to use to download files in parallel.
        """
        ...


class Dataset(Protocol):
    """Class wrapper around Offline Query results.
    Datasets are obtained by invoking `ChalkClient.offline_query()`.
    `Dataset` instances store important metadata and enable the retrieval of
    offline query outputs.

    >>> from chalk.client import ChalkClient, Dataset
    >>> uids = [1, 2, 3, 4]
    >>> at = datetime.now()
    >>> dataset: Dataset = ChalkClient().offline_query(
    ...     input={
    ...         User.id: uids,
    ...         User.ts: [at] * len(uids),
    ...     },
    ...     output=[
    ...         User.id,
    ...         User.fullname,
    ...         User.email,
    ...         User.name_email_match_score,
    ...     ],
    ...     dataset_name='my_dataset'
    ... )
    >>> df = dataset.get_data_as_pandas()
    >>> df.recompute(features=[User.fraud_score], branch="feature/testing")
    """

    is_finished: bool
    """Whether the most recent `DatasetRevision` is finished or still pending."""

    version: int
    """Storage version number of outputs."""

    revisions: List[DatasetRevision]
    """A list of all `DatasetRevision` instances belonging to this dataset."""

    dataset_name: Optional[str]
    """The unique name for this dataset, if given."""

    dataset_id: Optional[uuid.UUID]
    """The unique UUID for this dataset."""

    errors: Optional[List[ChalkError]]
    """A list of errors in loading the dataset, if they exist."""

    def get_data_as_polars(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pl.LazyFrame:
        """Loads a `pl.LazyFrame` containing the output of the most recent revision.

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pl.LazyFrame`.
        output_ts
            Whether to return the timestamp feature in a column
            named `__chalk__.CHALK_TS` in the resulting `pl.LazyFrame`.

        Returns
        -------
        pl.LazyFrame
            a `pl.LazyFrame` materializing query output data.
        """
        ...

    def get_data_as_pandas(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> pd.DataFrame:
        """Loads a `pd.DataFrame` containing the output of the most recent revision.

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `pd.DataFrame`.
        output_ts
            Whether to return the timestamp feature in a column
            named `__chalk__.CHALK_TS` in the resulting `pd.DataFrame`.

        Returns
        -------
        pd.DataFrame
            a `pd.DataFrame` materializing query output data.
        """
        ...

    def get_data_as_dataframe(
        self,
        output_id: bool = False,
        output_ts: bool = False,
    ) -> DataFrame:
        """Loads a Chalk `DataFrame` containing the output of the most recent revision.

        Other Parameters
        ----------
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `DataFrame`.
        output_ts
            Whether to return the timestamp feature in a column
            named `__chalk__.CHALK_TS` in the resulting `DataFrame`.

        Returns
        -------
        DataFrame
            A `DataFrame` materializing query output data.
        """
        ...

    def download_data(
        self,
        path: str,
        num_executors: Optional[int] = None,
    ) -> None:
        """Downloads output files pertaining to the revision to given path.

        Datasets are stored in Chalk as sharded Parquet files. With this
        method, you can download those raw files into a directory for processing
        with other tools.

        Parameters
        ----------
        path
            A directory where the Parquet files from the dataset will be downloaded.

        Other Parameters
        ----------
        num_executors
            Number of executors to use to download files in parallel.

        Examples
        ----------
        >>> from chalk.client import ChalkClient, Dataset
        >>> uids = [1, 2, 3, 4]
        >>> at = datetime.now()
        >>> dataset: Dataset = ChalkClient().offline_query(
        ...     input={
        ...         User.id: uids,
        ...         User.ts: [at] * len(uids),
        ...     },
        ...     output=[
        ...         User.id,
        ...         User.fullname,
        ...         User.email,
        ...         User.name_email_match_score,
        ...     ],
        ...     dataset_name='my_dataset'
        ... )
        >>> dataset.download_data('my_directory')
        """
        ...

    def recompute(self, branch: BranchId, features: Optional[List[Union[Feature, Any]]]):
        """Creates a new revision of this dataset by recomputing the specified features.

        Carries out the new computation on the specified branch.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> dataset = ChalkClient(branch="data_science").offline_query(...)
        >>> df = dataset.get_data_as_polars()
        >>> # change some resolvers
        >>> dataset.recompute(branch="data_science")
        >>> new_df = dataset.get_data_as_polars() # receive newly computed data
        """
        ...


class OnlineQueryResult(Protocol):
    data: List[FeatureResult]
    """The output features and any query metadata."""

    errors: Optional[List[ChalkError]]
    """Errors encountered while running the resolvers.

    If no errors were encountered, this field is empty.
    """

    def get_feature(self, feature: Union[str, Any]) -> Optional[FeatureResult]:
        """Convenience method for accessing feature result from the data response

        Parameters
        ----------
        feature
            The feature or its string representation.

        Returns
        -------
        FeatureResult | None
            The `FeatureResult` for the feature, if it exists.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> data = ChalkClient().query(...)
        >>> data.get_feature(User.name).ts
        datetime.datetime(2023, 2, 5, 23, 25, 26, 427605)
        >>> data.get_feature("user.name").meta.cache_hit
        False
        """
        ...

    def get_feature_value(self, feature: Any) -> Optional[Any]:
        """Convenience method for accessing feature values from the data response

        Parameters
        ----------
        feature
            The feature or its string representation.

        Returns
        -------
        Any
            The value of the feature.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> data = ChalkClient().query(...)
        >>> data.get_feature_value(User.name)
        "Katherine Johnson"
        >>> data.get_feature_value("user.name")
        "Katherine Johnson"
        """
        ...


class ChalkClient:
    """The `ChalkClient` is the primary interface for interacting with Chalk.

    You can use it to query data, trigger resolver runs, gather offline data, and more.
    """

    @overload
    def __init__(self, session: Optional[requests.Session] = None):
        """Create a `ChalkClient` with environment variables or credentials in `~/.chalk.yml`.

        The client will first check for the presence of the environment variables
        `CHALK_CLIENT_ID` and `CHALK_CLIENT_SECRET`. If they are present,
        `ChalkClient` will use those credentials, and optionally the API server
        and environment specified by `CHALK_API_SERVER` and `CHALK_ENVIRONMENT`.

        Otherwise, it will look for a `~/.chalk.yml` file, which is updated
        when you run `chalk login`. If a token for the specific project directory
        if found, that token will be used. Otherwise, the token under the key
        `default` will be used. When using the `~/.chalk.yml` file, you can still
        optionally override the API server and environment by setting the
        environment variables `CHALK_API_SERVER` and `CHALK_ENVIRONMENT`.

        Parameters
        ----------
        session
            A `requests.Session` to use for all requests. If not provided,
            a new session will be created.


        Raises
        ------
        ChalkAuthException
            If `client_id` or `client_secret` are not provided, there
            is no `~/.chalk.yml` file with applicable credentials,
            and the environment variables `CHALK_CLIENT_ID` and
            `CHALK_CLIENT_SECRET` are not set.
        """
        ...

    @overload
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        environment: Optional[EnvironmentId] = None,
        api_server: Optional[str] = None,
        branch: Optional[BranchId] = None,
        session: Optional[requests.Session] = None,
    ):
        """Create a `ChalkClient` with the given credentials.

        Parameters
        ----------
        client_id
            The client ID to use to authenticate. Can either be a
            service token id or a user token id.
        client_secret
            The client secret to use to authenticate. Can either be a
            service token secret or a user token secret.
        environment
            The ID or name of the environment to use for this client.
            Not necessary if your `client_id` and `client_secret`
            are for a service token scoped to a single environment.
            If not present, the client will use the environment variable
            `CHALK_ENVIRONMENT`.
        api_server
            The API server to use for this client. Required if you are
            using a Chalk Dedicated deployment. If not present, the client
            will check for the presence of the environment variable
            `CHALK_API_SERVER`, and use that if found.
        branch
            If specified, Chalk will route all requests from this client
            instance to the relevant branch. Some methods allow you to
            override this instance-level branch configuration by passing
            in a `branch` argument.
        session
            A `requests.Session` to use for all requests. If not provided,
            a new session will be created.

        Raises
        ------
        ChalkAuthException
            If `client_id` or `client_secret` are not provided, there
            is no `~/.chalk.yml` file with applicable credentials,
            and the environment variables `CHALK_CLIENT_ID` and
            `CHALK_CLIENT_SECRET` are not set.
        """
        ...

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: Optional[EnvironmentId] = None,
        api_server: Optional[str] = None,
        branch: Optional[BranchId] = None,
        session: Optional[requests.Session] = None,
    ):
        """Create a `ChalkClient`. Clients can either be created
        explicitly, with environment variables, or using credentials
        in `~/.chalk.yml`.

        The `__init__` method specifies overloads for this purpose.
        See the overloaded methods for details.
        """
        ...

    def trigger_resolver_run(
        self,
        resolver_fqn: str,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = None,
    ) -> ResolverRunResponse:
        """Triggers a resolver to run.
        See https://docs.chalk.ai/docs/runs for more information.

        Parameters
        ----------
        resolver_fqn
            The fully qualified name of the resolver to trigger.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        preview_deployment_id
            If specified, Chalk will route your request to the
            relevant preview deployment.
        branch

        Returns
        -------
        ResolverRunResponse
            Status of the resolver run and the run ID.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().trigger_resolver_run(
        ...     resolver_fqn="mymodule.fn"
        ... )
        """
        ...

    def get_run_status(
        self,
        run_id: str,
        environment: Optional[EnvironmentId] = None,
        preview_deployment_id: Optional[str] = None,
        branch: Optional[BranchId] = None,
    ) -> ResolverRunResponse:
        """Retrieves the status of a resolver run.
        See https://docs.chalk.ai/docs/runs for more information.

        Parameters
        ----------
        run_id
            ID of the resolver run to check.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        preview_deployment_id
            If specified, Chalk will route your request to the
            relevant preview deployment.
        branch

        Returns
        -------
        ResolverRunResponse
            Status of the resolver run and the run ID.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().get_run_status(
        ...     run_id="3",
        ... )
        ResolverRunResponse(
            id="3",
            status=ResolverRunStatus.SUCCEEDED
        )
        """
        ...

    def whoami(self) -> WhoAmIResponse:
        """Checks the identity of your client.

        Useful as a sanity test of your configuration.

        Returns
        -------
        WhoAmIResponse
            The identity of your client.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().whoami()
        WhoAmIResponse(user="44")
        """
        ...

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
    ) -> OnlineQueryResult:
        """Compute features values using online resolvers.
        See https://docs.chalk.ai/docs/query-basics for more information.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to those values.
        output
            Outputs are the features that you'd like to compute from the inputs.
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        tags
            The tags used to scope the resolvers.
            More information at https://docs.chalk.ai/docs/resolver-tags
        branch
            If specified, Chalk will route your request to the relevant branch.
        preview_deployment_id
            If specified, Chalk will route your request to the
            relevant preview deployment.

        Other Parameters
        ----------------
        query_name
            The name for class of query you're making, for example, "loan_application_model".
        correlation_id
            A globally unique ID for the query, used alongside logs and
            available in web interfaces. If None, a correlation ID will be
            generated for you and returned on the response.
        meta
            Arbitrary `key:value` pairs to associate with a query.
        context
            Deprecated in favor of `environment` and `tags`.

        Returns
        -------
        OnlineQueryResult
            The outputs features and any query metadata,
            plus errors encountered while running the resolvers.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        ... ChalkClient().query(
        ...     input={User.name: "Katherine Johnson"},
        ...     output=[User.fico_score],
        ...     staleness={User.fico_score: "10m"},
        ... )
        """
        ...

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
        """Upload data to Chalk for use in offline resolvers or to prime a cache.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to those values.
        branch
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        preview_deployment_id
            If specified, Chalk will route your request to the relevant preview deployment
        query_name
            Optionally associate this upload with a query name. See `.query` for more information.

        Other Parameters
        ----------------
        correlation_id
            A globally unique ID for this operation, used alongside logs and
            available in web interfaces. If None, a correlation ID will be
            generated for you and returned on the response.
        meta
            Arbitrary key:value pairs to associate with a query.

        Returns
        -------
        list[ChalkError] | None
            The errors encountered from uploading features.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().upload_features(
        ...     input={
        ...         User.id: 1,
        ...         User.name: "Katherine Johnson"
        ...     }
        ... )
        """
        ...

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
    ) -> Dataset:
        """Compute feature values from the offline store.
        See `Dataset` for more information.

        Parameters
        ----------
        input
            The features for which there are known values.
            It can be a mapping of features to a list of values for each
            feature, or an existing `DataFrame`.
            Each element in the `DataFrame` or list of values represents
            an observation in line with the timestamp in `input_times`.
        input_times
            A list of the times of the observations from `input`.
        output
            The features that you'd like to sample, if they exist.
            If an output feature was never computed for a sample (row) in
            the resulting `DataFrame`, its value will be `None`.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        dataset_name
            A unique name that if provided will be used to generate and
            save a `Dataset` constructed from the list of features computed
            from the inputs.
        max_samples
            The maximum number of samples to include in the `DataFrame`.
            If not specified, all samples will be returned.
        branch

        Other Parameters
        ----------------
        required_output
            The features that you'd like to sample and must exist
            in each resulting row. Rows where a `required_output`
            was never stored in the offline store will be skipped.
            This differs from specifying the feature in `output`,
            where instead the row would be included, but the feature
            value would be `None`.

        Returns
        -------
        Dataset
            A Chalk `Dataset`.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> uids = [1, 2, 3, 4]
        >>> at = datetime.now()
        >>> dataset = ChalkClient().offline_query(
        ...     input={
        ...         User.id: uids,
        ...         User.ts: [at] * len(uids),
        ...     },
        ...     output=[
        ...         User.id,
        ...         User.fullname,
        ...         User.email,
        ...         User.name_email_match_score,
        ...     ],
        ...     dataset_name='my_dataset'
        ... )
        >>> df = dataset.get_data_as_pandas()
        """
        ...

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
        """Deprecated. Use `.offline_query` instead.

        Compute feature values from the offline store.
        See https://docs.chalk.ai/docs/training-client for more information.

        Parameters
        ----------
        input
            The features for which there are known values.
            It can be a mapping of features to a list of values for each
            feature, or an existing `DataFrame`.
            Each element in the `DataFrame` or list of values represents
            an observation in line with the timestamp in `input_times`.
        input_times
            A list of the times of the observations from `input`.
        output
            The features that you'd like to sample, if they exist.
            If an output feature was never computed for a sample (row) in
            the resulting `DataFrame`, its value will be `None`.
        context
            The environment under which you'd like to query your data.
        dataset
            A unique name that if provided will be used to generate and
            save a dataset constructed from the list of features computed
            from the inputs.
        max_samples
            The maximum number of samples to include in the `DataFrame`.
            If not specified, all samples will be returned.

        Other Parameters
        ----------------
        required_output
            The features that you'd like to sample and must exist
            in each resulting row. Rows where a `required_output`
            was never stored in the offline store will be skipped.
            This differs from specifying the feature in `output`,
            where instead the row would be included, but the feature
            value would be `None`.
        output_ts
            Whether to return the timestamp feature in a column
            named `__chalk__.CHALK_TS` in the resulting `DataFrame`.

        Returns
        -------
        pd.DataFrame
            A `pandas.DataFrame` with columns equal to the names of the
            features in output, and values representing the value of the
            observation for each input time.
            The output maintains the ordering from `input`

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> uids = [1, 2, 3, 4]
        >>> at = datetime.now()
        >>> X = ChalkClient().get_training_dataframe(
        ...     input={
        ...         User.id: uids,
        ...         User.ts: [at] * len(uids),
        ...     },
        ...     output=[
        ...         User.id,
        ...         User.fullname,
        ...         User.email,
        ...         User.name_email_match_score,
        ...     ],
        ... )
        """
        ...

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
        """Get the most recent feature values from the offline store.

        See https://docs.chalk.ai/docs/training-client for more information.

        Parameters
        ----------
        output
            The features that you'd like to sample, if they exist.
            If an output feature was never computed for a sample (row)
            in the resulting `DataFrame`, its value will be `None`.
        max_samples
            The maximum number of rows to return.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.
        dataset
            The `Dataset` name under which to save the output.
        branch

        Other Parameters
        ----------------
        required_output
            The features that you'd like to sample and must exist
            in each resulting row. Rows where a `required_output`
            was never stored in the offline store will be skipped.
            This differs from specifying the feature in `output`,
            where instead the row would be included, but the feature
            value would be `None`.
        output_ts
            Whether to return the timestamp feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `DataFrame`.
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `DataFrame`.

        Returns
        -------
        pd.DataFrame
            A `pandas.DataFrame` with columns equal to the names of the features in output,
            and values representing the value of the most recent observation.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> sample_df = ChalkClient().sample(
        ...     output=[
        ...         Account.id,
        ...         Account.title,
        ...         Account.user.full_name
        ...     ],
        ...     max_samples=10
        ... )
        """
        ...

    def get_dataset(
        self,
        dataset_name: str,
        environment: Optional[EnvironmentId] = None,
    ) -> Dataset:
        """Get a Chalk `Dataset` containing data from a previously created dataset.

        If an offline query has been created with a dataset name, `.get_dataset` will
        return a Chalk `Dataset`.
        The `Dataset` wraps a lazily-loading Chalk `DataFrame` that enables us to analyze
        our data without loading all of it directly into memory.
        See https://docs.chalk.ai/docs/training-client for more information.

        Parameters
        ----------
        dataset_name
            The name of the `Dataset` to return.
            Previously, you must have supplied a dataset name upon an offline query.
            Dataset names are unique for each environment.
        environment
            The environment under which to run the resolvers.
            API tokens can be scoped to an environment.
            If no environment is specified in the query,
            but the token supports only a single environment,
            then that environment will be taken as the scope
            for executing the request.

        Returns
        -------
        Dataset
            A `Dataset` that lazily loads your query data.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> uids = [1, 2, 3, 4]
        >>> at = datetime.now()
        >>> X = ChalkClient().get_training_dataframe(
        ...     input={
        ...         User.id: uids,
        ...         User.ts: [at] * len(uids),
        ...     },
        ...     output=[
        ...         User.id,
        ...         User.fullname,
        ...         User.email,
        ...         User.name_email_match_score,
        ...     ],
        ...     dataset='my_dataset_name'
        ... )

        Some time later...

        >>> dataset = ChalkClient().get_dataset(
        ...     dataset_name='my_dataset_name'
        ... )
        ...

        If memory allows:

        >>> df: pd.DataFrame = dataset.get_data_as_pandas()
        """
        ...

    def __new__(cls, *args: Any, **kwargs: Any):
        from chalk.client.client_impl import ChalkAPIClientImpl

        return ChalkAPIClientImpl(*args, **kwargs)


ChalkAPIClientProtocol: TypeAlias = ChalkClient
"""Deprecated. Use `ChalkClient` instead."""

__all__ = [
    "ChalkAPIClientProtocol",
    "ChalkBaseException",
    "ChalkClient",
    "ChalkAuthException",
    "ChalkDatasetDownloadException",
    "ChalkError",
    "ChalkException",
    "ChalkOfflineQueryException",
    "ChalkResolverRunException",
    "Dataset",
    "DatasetRevision",
    "ErrorCode",
    "ErrorCodeCategory",
    "FeatureResult",
    "OfflineQueryContext",
    "OnlineQueryContext",
    "OnlineQueryResponse",
    "OnlineQueryResult",
    "QueryStatus",
    "ResolverRunResponse",
    "WhoAmIResponse",
]
