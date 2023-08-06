import aiohttp

from bovine.utils.parse import parse_fediverse_handle

from .lookup_account import lookup_with_webfinger  # noqa F401


async def lookup_account_with_webfinger(
    session: aiohttp.ClientSession, fediverse_handle: str
) -> str | None:
    """Looks up the actor url associated with a FediVerse handle,
    i.e. an identifier of the form username@domain, using
    the webfinger endpoint

    :param session: the aiohttp.ClientSession to use
    :param fediverse_handle: the FediVerse handle as a string
    """
    username, domain = parse_fediverse_handle(fediverse_handle)

    webfinger_url = f"https://{domain}/.well-known/webfinger"
    params = {"resource": f"acct:{username}@{domain}"}

    return await lookup_with_webfinger(session, webfinger_url, params)


async def lookup_did_with_webfinger(
    session: aiohttp.ClientSession, domain: str, did: str
) -> str | None:
    """Looks up the actor url associated with a did and domain
    using the webfinger endpoint

    :param session: the aiohttp.ClientSession to use
    :param domain: the domain to perform the lookup from
    :param did: the did key to perform lookup with
    """
    webfinger_url = f"https://{domain}/.well-known/webfinger"
    params = {"resource": did}

    return await lookup_with_webfinger(session, webfinger_url, params)
