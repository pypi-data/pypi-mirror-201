import abc
from typing import List, Optional

from chalk.client.models import ChalkError


class ChalkBaseException(Exception, abc.ABC):
    """The base type for Chalk exceptions.

    This exception makes error handling easier, as you can
    look only for this exception class.
    """

    errors: List[ChalkError]
    """The errors from executing a Chalk operation.

    These errors contain more detailed information about
    why the exception occurred.
    """

    def __init__(self, errors: Optional[List[ChalkError]] = None):
        if errors is None:
            errors = []

        self.errors = errors

        super().__init__(self.full_message)

    @property
    def message(self) -> str:
        """A message describing the specific type of exception raised."""
        raise NotImplementedError

    @property
    def full_message(self) -> str:
        """A message that describes the specific type of exception raised
        and contains the readable representation of each error in the
        errors attribute.
        """
        if self.errors:
            return self.message + "\n" + "\n".join(["\t" + e.message for e in self.errors])

        return self.message


class ChalkWhoAmIException(ChalkBaseException):
    """Raised from the `ChalkClient.whoami` method."""

    @property
    def message(self) -> str:
        return "Failed to retrieve current user information during `whoami` check"


class ChalkOnlineQueryException(ChalkBaseException):
    @property
    def message(self) -> str:
        return "Failed to execute online query"


class ChalkOfflineQueryException(ChalkBaseException):
    @property
    def message(self) -> str:
        return "Failed to execute offline query"

    @property
    def full_message(self) -> str:
        return self.message + "\n" + "\n".join(["\t" + e.message for e in self.errors[0:3]])


class ChalkComputeResolverException(ChalkOfflineQueryException):
    """Exception raised when failing to compute the resolver output."""

    @property
    def message(self) -> str:
        return "Failed to compute resolver output"


class ChalkResolverRunException(ChalkBaseException):
    """Raised when failing to get the resolver's status via `ChalkClient.get_run_status`"""

    @property
    def message(self) -> str:
        return "Resolver run failed"


class ChalkUpdateResolverException(ChalkBaseException):
    """Raised when failing to update a resolver on the fly from a notebook"""

    @property
    def message(self) -> str:
        return "Failed to update resolver."


class ChalkRecomputeDatasetException(ChalkBaseException):
    def __init__(self, dataset_name: str, errors: Optional[List[ChalkError]] = None):
        self.dataset_name = dataset_name
        super().__init__(errors)

    @property
    def message(self) -> str:
        return f"Failed to recompute dataset '{self.dataset_name}'"


class ChalkDatasetDownloadException(ChalkBaseException):
    def __init__(self, dataset_name: str, errors: Optional[List[ChalkError]] = None):
        self.dataset_name = dataset_name
        super().__init__(errors)

    @property
    def message(self) -> str:
        return f"Failed to download dataset '{self.dataset_name}'"

    @property
    def full_message(self) -> str:
        return self.message + "\n" + "\n".join(["\t" + e.message for e in self.errors])


class ChalkAuthException(ChalkBaseException):
    """Raised when constructing a `ChalkClient` without valid credentials.

    When this exception is raise, no explicit `client_id` and `client_secret`
    were provided, there was no `~/.chalk.yml` file with applicable credentials,
    and the environment variables `CHALK_CLIENT_ID` and `CHALK_CLIENT_SECRET`
    were not set.

    You may need to run `chalk login` from your command line, or check that your
    working directory is set to the root of your project.
    """

    @property
    def message(self):
        return (
            "Explicit `client_id` and `client_secret` are not provided, "
            "there is no `~/.chalk.yml` file with applicable credentials, "
            "and the environment variables `CHALK_CLIENT_ID` and "
            "`CHALK_CLIENT_SECRET` are not set. "
            "You may need to run `chalk login` from your command line, "
            "or check that your working directory is set to the root of "
            "your project."
        )


__all__ = [
    "ChalkBaseException",
    "ChalkOnlineQueryException",
    "ChalkOfflineQueryException",
    "ChalkResolverRunException",
    "ChalkDatasetDownloadException",
    "ChalkComputeResolverException",
    "ChalkAuthException",
    "ChalkWhoAmIException",
]
