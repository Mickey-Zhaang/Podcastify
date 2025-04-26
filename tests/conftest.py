"""
Defines fixtures: Conftest.py
"""

import pytest
from website import create_app


@pytest.fixture
def app(monkeypatch):
    """
    App
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["OPENAI_API_KEY"] = "dummy_key"
    app.config["PROPAGATE_EXCEPTIONS"] = False
    app.config["SECRET_KEY"] = "secret"
    return app


@pytest.fixture(scope="function")
def client(app):
    """
    Pytest Fixture:
        Yields a client for testing!
        Fixture name: client
    """
    with app.test_client() as test_client:
        yield test_client
