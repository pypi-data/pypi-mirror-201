import asyncio
from http import HTTPStatus
from typing import List, Optional

from aiohttp import ClientConnectionError, ClientResponseError

from anyscale.api_utils.exceptions.log_retrieval_errors import (
    LogNotFoundOnActiveClusterError,
    UnsupportedLogRetrievalMethodError,
    wrap_as_unsupported_log_retrieval_method_error,
)
from anyscale.api_utils.job_util import _get_job_run_id
from anyscale.api_utils.logs_util import (
    _download_log_from_ray_json_response,
    _download_logs_concurrently,
    _remove_ansi_escape_sequences,
)
from anyscale.controllers.logs_controller import DEFAULT_PARALLELISM
from anyscale.sdk.anyscale_client.api.default_api import DefaultApi as BaseApi
from anyscale.sdk.anyscale_client.models.log_download_result import LogDownloadResult


async def _get_logs_from_running_job(
    base_api: BaseApi, job_run_id: str, remove_escape_chars: bool = True
) -> str:
    with wrap_as_unsupported_log_retrieval_method_error():
        job_logs_url: str = base_api.get_job_logs_stream(
            job_id=job_run_id
        ).result.http_url
    try:
        logs = await _download_log_from_ray_json_response(job_logs_url)
        if remove_escape_chars:
            logs = _remove_ansi_escape_sequences(logs)
        return logs
    except (ClientConnectionError, asyncio.TimeoutError):
        raise UnsupportedLogRetrievalMethodError(
            f'Streaming logs is only supported if the Anyscale SDK client can reach the cluster running the job "{job_run_id}". '
            "Check that the client is running on the same private network (may be protected behind VPN)."
        )
    except ClientResponseError as e:
        # Will return 404 if job run (Ray job) is not found
        # https://github.com/ray-project/ray/blob/6334576223dd916469fcdac185752b80e0c3e416/dashboard/modules/job/job_head.py#L485
        if e.status == HTTPStatus.NOT_FOUND:
            raise LogNotFoundOnActiveClusterError(
                f'Job "{job_run_id}" is not a part of the current active session of the cluster. '
                "The cluster may have restarted since the job ran."
            )
        raise e


async def _get_job_logs_from_storage_bucket(
    base_api: BaseApi,
    *,
    job_id: Optional[str] = None,
    job_run_id: Optional[str] = None,
    parallelism: int = DEFAULT_PARALLELISM,
    remove_escape_chars: bool = True,
) -> str:
    with wrap_as_unsupported_log_retrieval_method_error():
        job_run_id = _get_job_run_id(base_api, job_id=job_id, job_run_id=job_run_id)
        all_log_chunk_urls: List[str] = []

        log_download_result: LogDownloadResult = base_api.get_job_logs_download(
            job_id=job_run_id, all_logs=True
        ).result
        for log_chunk in log_download_result.log_chunks:
            all_log_chunk_urls.append(log_chunk.chunk_url)
    logs = await _download_logs_concurrently(all_log_chunk_urls, parallelism)
    if remove_escape_chars:
        logs = _remove_ansi_escape_sequences(logs)
    return logs


async def _get_logs_from_running_production_job(
    base_api: BaseApi, production_job_id: str, remove_escape_chars: bool = True,
) -> str:
    with wrap_as_unsupported_log_retrieval_method_error():
        last_job_run_id = _get_job_run_id(base_api, job_id=production_job_id)
    return await _get_logs_from_running_job(
        base_api, last_job_run_id, remove_escape_chars
    )
