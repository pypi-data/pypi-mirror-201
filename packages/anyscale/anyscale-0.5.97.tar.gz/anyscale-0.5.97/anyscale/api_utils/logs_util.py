import asyncio
import re
from typing import List

import aiohttp

from anyscale.shared_anyscale_utils.utils.asyncio import gather_in_batches


async def _download_logs_concurrently(
    log_chunk_urls: List[str], parallelism: int
) -> str:
    logs_across_chunks = await gather_in_batches(
        parallelism, *[_download_log_from_s3_url(url) for url in log_chunk_urls]
    )
    return "".join(logs_across_chunks)  # type: ignore


async def _download_log_from_ray_json_response(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        response = await asyncio.wait_for(session.get(url), timeout=30)
        logs: str = (await response.json()).get("logs", "")
        return logs


async def _download_log_from_s3_url(url: str) -> str:
    # Note that the URL is presigned, so no token needs to be passed in the request
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def _remove_ansi_escape_sequences(s: str) -> str:
    # Required as the log may contain ANSI escape sequeneces (e.g. for coloring in the terminal)
    # Regex pattern from https://stackoverflow.com/a/14693789
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", s)
