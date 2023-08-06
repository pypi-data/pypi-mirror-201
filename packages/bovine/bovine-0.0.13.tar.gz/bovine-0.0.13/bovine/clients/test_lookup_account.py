import aiohttp

from . import lookup_account_with_webfinger, lookup_did_with_webfinger


async def test_lookup_account():
    async with aiohttp.ClientSession() as session:
        result = await lookup_account_with_webfinger(session, "helge@mymath.rocks")

    assert result.startswith("https://mymath.rocks/")


async def test_lookup_did_with_webfinger():
    did_helge = "did:key:z6MkujdZ216eYz55vz8X5HetqeJXj9ddn5ZHZUsBpRX4wfnL"
    async with aiohttp.ClientSession() as session:
        result = await lookup_did_with_webfinger(session, "mymath.rocks", did_helge)

    assert result.startswith("https://mymath.rocks/")
