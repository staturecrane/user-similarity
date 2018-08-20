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


def test_user(client):
    similar_user_query = client.get('/user/similarity/1')
    assert similar_user_query.status_code == 200
    assert similar_user_query.get_data()

    similar_users = json.loads(similar_user_query.get_data(as_text=True))
    assert len(similar_users) == 10

    bad_user_query = client.get('/user/similarity/10001')
    assert bad_user_query.status_code == 400

