from fastapi.testclient import TestClient

from dilife.app import app


def test_root_must_return_200():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}
