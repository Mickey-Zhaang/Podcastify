"""
Testing views.py
"""


def test_home_route(client):
    """
    GIVEN some client
    WHEN '/' is requested
    THEN check the functionality
    """
    response = client.get("/")

    assert response.status_code == 200
    assert b"Podcastify" in response.data


def test_redirects_when_not_logged_in(client):
    """
    GIVEN some client
    WHEN '/start-process' is requested
    THEN check no 'credentials' in session → redirect to /index and a flash message
    """

    response = client.post("/start-process", follow_redirects=False)
    assert response.status_code == 200
    assert b"Please log in before Podcastifying!" in response.data


def test_internal_error_if_service_fails(monkeypatch, client):
    """
    GIVEN some client
    WHEN '/start-process' is requested with no creds
    THEN check proper failure if no service fails
    """
    with client.session_transaction() as sess:
        sess["credentials"] = {"token": "token", "refresh_token": "lol"}

    def fake_build(creds):
        raise RuntimeError("API down")

    monkeypatch.setattr("website.views.build_service", fake_build)

    response = client.post("/start-process")
    assert response.status_code == 500


def test_successful_render(monkeypatch, client):
    """
    GIVEN some client
    WHEN '/start-process/ is requested with proper creds
    THEN check proper functionality (check comments)
    """
    with client.session_transaction() as sess:
        sess["credentials"] = {"token": "token", "refresh_token": "rf_token"}

    monkeypatch.setattr("website.views.build_service", lambda creds: object())
    monkeypatch.setattr("website.views.list_past_message_ids", lambda svc: ["m1", "m2"])
    monkeypatch.setattr("website.views.get_top_k_messages", lambda k, ids, svc: ["hello", "world"])
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    monkeypatch.setattr("website.views.podcastify", lambda msgs, key: "EPISODE 1 SUMMARY")
    resp = client.post("/start-process")
    assert resp.status_code == 200
    assert b"EPISODE 1 SUMMARY" in resp.data
