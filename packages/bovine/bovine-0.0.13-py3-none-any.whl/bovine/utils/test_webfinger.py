from .webfinger import webfinger_response_json


def test_webfinger():
    response = webfinger_response_json("name", "url", "domain")

    assert "subject" in response
    assert "links" in response
