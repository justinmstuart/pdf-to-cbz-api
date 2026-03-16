import io
import pytest
from unittest.mock import patch

from constants.errors import Errors

TEST_SECRET = 'test-secret'
AUTH_HEADERS = {'Authorization': f'Bearer {TEST_SECRET}'}


@pytest.fixture(autouse=True)
def mock_auth():
    with patch('middleware.auth.Env') as mock_env:
        mock_env.API_SECRET = TEST_SECRET
        yield mock_env


def test_no_file_in_request_returns_400(client):
    response = client.post('/pdf-to-cbz/', headers=AUTH_HEADERS)
    assert response.status_code == 400
    assert response.get_json()['error'] == Errors.INVALID_REQUEST_NO_FILE


def test_empty_filename_returns_400(client):
    data = {'file': (io.BytesIO(b''), '', 'application/pdf')}
    response = client.post(
        '/pdf-to-cbz/',
        headers=AUTH_HEADERS,
        data=data,
        content_type='multipart/form-data',
    )
    assert response.status_code == 400
    assert response.get_json()['error'] == Errors.INVALID_REQUEST_NO_FILE


def test_invalid_file_extension_returns_400(client):
    data = {'file': (io.BytesIO(b'fake content'), 'test.txt', 'text/plain')}
    response = client.post(
        '/pdf-to-cbz/',
        headers=AUTH_HEADERS,
        data=data,
        content_type='multipart/form-data',
    )
    assert response.status_code == 400
    assert response.get_json()['error'] == Errors.INVALID_FILE_TYPE


def test_invalid_mimetype_returns_400(client):
    data = {'file': (io.BytesIO(b'fake content'), 'test.pdf', 'text/plain')}
    response = client.post(
        '/pdf-to-cbz/',
        headers=AUTH_HEADERS,
        data=data,
        content_type='multipart/form-data',
    )
    assert response.status_code == 400
    assert response.get_json()['error'] == Errors.INVALID_FILE_TYPE


def test_conversion_exception_returns_500(client, tmp_path):
    def fake_save(file, filename, directory):
        return str(tmp_path / filename)

    with patch('blueprints.pdf_to_cbz_bp.process_pdf_files', side_effect=Exception('Conversion error')), \
         patch('blueprints.pdf_to_cbz_bp.save_file_to_directory', side_effect=fake_save):
        data = {'file': (io.BytesIO(b'%PDF fake'), 'test.pdf', 'application/pdf')}
        response = client.post(
            '/pdf-to-cbz/',
            headers=AUTH_HEADERS,
            data=data,
            content_type='multipart/form-data',
        )
    assert response.status_code == 500
    assert 'Conversion error' in response.get_json()['error']


def test_missing_cbz_after_conversion_returns_500(client, tmp_path):
    def fake_save(file, filename, directory):
        return str(tmp_path / filename)

    with patch('blueprints.pdf_to_cbz_bp.process_pdf_files'), \
         patch('blueprints.pdf_to_cbz_bp.save_file_to_directory', side_effect=fake_save):
        data = {'file': (io.BytesIO(b'%PDF fake'), 'test.pdf', 'application/pdf')}
        response = client.post(
            '/pdf-to-cbz/',
            headers=AUTH_HEADERS,
            data=data,
            content_type='multipart/form-data',
        )
    assert response.status_code == 500
    assert response.get_json()['error'] == Errors.CONVERSION_FAILED


def test_successful_conversion_returns_cbz(client, tmp_path):
    cbz_file = tmp_path / 'test.cbz'
    cbz_file.write_bytes(b'PK\x03\x04fake cbz content')

    def fake_save(file, filename, directory):
        return str(tmp_path / filename)

    with patch('blueprints.pdf_to_cbz_bp.process_pdf_files'), \
         patch('blueprints.pdf_to_cbz_bp.save_file_to_directory', side_effect=fake_save), \
         patch('blueprints.pdf_to_cbz_bp.delete_directory'):
        data = {'file': (io.BytesIO(b'%PDF fake'), 'test.pdf', 'application/pdf')}
        response = client.post(
            '/pdf-to-cbz/',
            headers=AUTH_HEADERS,
            data=data,
            content_type='multipart/form-data',
        )
    assert response.status_code == 200
    assert response.content_type == 'application/vnd.comicbook+zip'
    assert response.data == b'PK\x03\x04fake cbz content'
