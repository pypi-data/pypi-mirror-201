from contextlib import contextmanager
from http import HTTPStatus
import json
from typing import Generator, Optional

from anyscale_client.exceptions import ApiException

from anyscale.api_utils.exceptions.job_errors import NoJobRunError


class ExpectedLogRetrievalError(Exception):
    pass


class UnsupportedLogRetrievalMethodError(ExpectedLogRetrievalError):
    pass


class LogRetrievalTimeoutError(ExpectedLogRetrievalError):
    pass


class LogNotFoundOnActiveClusterError(ExpectedLogRetrievalError):
    pass


@contextmanager
def wrap_as_unsupported_log_retrieval_method_error() -> Generator[None, None, None]:
    try:
        yield
    except NoJobRunError as e:
        raise UnsupportedLogRetrievalMethodError from e
    except ApiException as e:
        if e.status == HTTPStatus.BAD_REQUEST:
            raise UnsupportedLogRetrievalMethodError(_get_exception_message(e))
        raise e


def _get_exception_message(e: ApiException) -> Optional[str]:
    return json.loads(e.body).get("error", {}).get("detail")
