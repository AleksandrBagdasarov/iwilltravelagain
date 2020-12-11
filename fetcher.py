'''
This file makes asynchronous requests
To use this script, import the request function,
example of use "response = await request('GET', https://example.com)"
'''

import asyncio

import httpx
from httpx import Response
from loguru import logger



DEFAULT_HEADERS = {
  'cache-control': 'max-age=0',
  'dnt': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

async def request(method: str,
                  url: str,
                  allow_status_codes: list = (200, 404),
                  retries: int = 10,
                  proxies: str = None,
                  timeout: int = 90,
                  headers: dict = DEFAULT_HEADERS,
                  **kwargs) -> Response:
    for _ in range(retries + 1):
        logger.info(f'{method}: {proxies}, {url}')
        if proxies:
            async with httpx.AsyncClient(verify=False, timeout=timeout, headers=headers) as client:
                response = await client.request(method, url, **kwargs)
        else:
            async with httpx.AsyncClient(proxies=proxies, verify=False, timeout=timeout, headers=headers) as client:
                response = await client.request(method, url, **kwargs)
        try:
            assert response.status_code in allow_status_codes
            return response

        except AssertionError:
            logger.debug(f'{method}: {url} {response.status_code}')
            await asyncio.sleep(3)
