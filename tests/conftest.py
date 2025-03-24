'''
Defines fixtures: Conftest.py
'''
import pytest
from website import create_app

@pytest.fixture
def client():
    '''
    Pytest Fixture:
        Yields a client for testing!
        Fixture name: client
    '''
    app = create_app()
    app.config["TESTING"] = True
    app.config["OPENAI_API_KEY"] = "dummy_key"
    with app.test_client() as test_client:
        yield test_client
