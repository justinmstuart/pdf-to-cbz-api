import pytest
from unittest.mock import patch

TEST_SECRET = 'test-secret'


@pytest.fixture(autouse=True)
def set_api_secret():
    with patch('middleware.auth.Env') as mock_env:
        mock_env.API_SECRET = TEST_SECRET
        yield mock_env


def test_missing_auth_header_returns_401(client):
    response = client.post('/pdf-to-cbz/')
    assert response.status_code == 401


def test_wrong_token_returns_401(client):
    response = client.post('/pdf-to-cbz/', headers={'Authorization': 'Bearer wrong-token'})
    assert response.status_code == 401


def test_valid_token_passes_auth(client):
    response = client.post('/pdf-to-cbz/', headers={'Authorization': f'Bearer {TEST_SECRET}'})
    # Auth passes but no file in request → 400
    assert response.status_code == 400


def test_empty_token_returns_401(client):
    response = client.post('/pdf-to-cbz/', headers={'Authorization': 'Bearer '})
    assert response.status_code == 401
