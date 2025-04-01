'''
Defines fixtures: Conftest.py
'''
import pytest
from website import create_app

@pytest.fixture(scope="function")
def client():
    '''
    Pytest Fixture:
        Yields a client for testing!
        Fixture name: client
    '''
    fkask_app = create_app()
    fkask_app.config["TESTING"] = True
    fkask_app.config["OPENAI_API_KEY"] = "dummy_key"
    with fkask_app.test_client() as test_client:
        yield test_client
