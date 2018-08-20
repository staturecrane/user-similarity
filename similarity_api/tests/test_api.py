import json
import pytest
from similarity_api.main import APP


@pytest.fixture
def client():
    APP.config['TESTING'] = True
    client = APP.test_client()

    yield client


def test_hello(client):
    health = client.get('/health')
    assert health.status_code == 200