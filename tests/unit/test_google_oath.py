'''
google_oath.py
'''

from unittest.mock import MagicMock
from website.google_oauth import get_redirect_url


def test_get_redirect_url(monkeypatch):
    '''
    Returns a dummy url that I will confirm works
    '''
    fake_flow = MagicMock()
    fake_flow.authorization_url.return_value = ("dummy url", "test state")

    monkeypatch.setattr("website.google_oauth.create_flow", lambda: fake_flow)

    result = get_redirect_url()
    assert isinstance(result, dict)
    assert result.get("auth_url") == "dummy url"
    assert result.get("state") == "test state"
