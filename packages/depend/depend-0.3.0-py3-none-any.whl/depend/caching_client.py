from __future__ import annotations

import httpx
from loguru import logger


class CachingClient(httpx.AsyncClient):
    """Implements very simple request caching: we'll cache all requests forever."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__cache = {}

    async def get(self, url: httpx._types.URLTypes, *args, **kwargs) -> httpx.Response:
        if url in self.__cache:
            logger.debug("Returning cached response for url: {}", url)
            return self.__cache[url]

        response = await super().get(url, *args, **kwargs)
        self.__cache[url] = response
        logger.debug("Cached response for url: {}", url)
        return response
