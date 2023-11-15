from fastapi.testclient import TestClient
from pytest import fixture

from dilife.app import app


@fixture
def client():
    return TestClient(app)
