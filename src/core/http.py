# src/core/http.py

import httpx
from src.utils.logging import log_error

DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 3


async def fetch_json(
    url,
    method="GET",
    timeout=DEFAULT_TIMEOUT,
    retries=DEFAULT_RETRIES,
    **kwargs,
):
    """
    Resilient HTTP JSON fetcher with retries and timeouts.
    All scrapers should use this instead of raw httpx.
    """
    last_exc = None

    for attempt in range(1, retries + 1):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method,
                    url,
                    timeout=timeout,
                    **kwargs,
                )
                response.raise_for_status()
                return response.json()
        except Exception as exc:
            last_exc = exc
            log_error(
                f"HTTP error on {url} "
                f"(attempt {attempt}/{retries}): {exc}"
            )

    # If all retries fail, raise the last exception
    raise last_exc
