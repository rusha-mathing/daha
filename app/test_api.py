from fastapi.testclient import TestClient

from main import api


client = TestClient(api)


def test_index():
    response = client.get('/')
    assert response.json() == 'hehe'
