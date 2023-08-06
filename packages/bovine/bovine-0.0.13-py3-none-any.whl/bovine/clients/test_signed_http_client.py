from unittest.mock import AsyncMock

import aiohttp

from bovine.utils.test import get_user_keys

from .signed_http_client import SignedHttpClient


async def test_activity_pub_client_get():
    session = AsyncMock(aiohttp.ClientSession)
    url = "https://test_domain/test_path"
    public_key_url = "public_key_url"
    public_key, private_key = get_user_keys()
    session = AsyncMock(aiohttp.ClientSession)
    session.get = AsyncMock()

    client = SignedHttpClient(session, public_key_url, private_key)

    await client.get(url)

    session.get.assert_awaited_once()
