def webfinger_response_json(name, url, domain):
    """helper to generate a webfinger response"""
    return {
        "subject": f"acct:{name}@{domain}",
        "links": [
            {
                "href": url,
                "rel": "self",
                "type": "application/activity+json",
            }
        ],
    }
