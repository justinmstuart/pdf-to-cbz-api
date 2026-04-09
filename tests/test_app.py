from constants.config import ConfigKeys
from unittest.mock import patch
import os


def test_app_max_content_length_configured(app):
    assert app.config[ConfigKeys.MAX_CONTENT_LENGTH] is not None
    assert app.config[ConfigKeys.MAX_CONTENT_LENGTH] > 0


def test_app_max_form_memory_size_configured(app):
    assert app.config[ConfigKeys.MAX_FORM_MEMORY_SIZE] is not None
    assert app.config[ConfigKeys.MAX_FORM_MEMORY_SIZE] > 0


def test_pdf_to_cbz_blueprint_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert any('/pdf-to-cbz' in rule for rule in rules)


def test_cors_headers_present_on_simple_request(client):
    """Test that CORS headers are present on a simple GET request."""
    response = client.get('/pdf-to-cbz/', headers={'Origin': 'http://example.com'})
    # Should be 404 or 405 since GET is not allowed, but CORS headers should still be present
    assert 'Access-Control-Allow-Origin' in response.headers


def test_cors_headers_on_preflight_request(client):
    """Test that CORS headers are present on OPTIONS preflight request."""
    headers = {
        'Origin': 'http://example.com',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Authorization'
    }
    response = client.options('/pdf-to-cbz/', headers=headers)
    assert response.status_code in [200, 204]
    
    # Verify Access-Control-Allow-Origin is present and correct
    allow_origin = response.headers.get('Access-Control-Allow-Origin')
    assert allow_origin is not None
    assert allow_origin in ('*', headers['Origin'])
    
    # Verify Access-Control-Allow-Methods includes POST
    allow_methods = response.headers.get('Access-Control-Allow-Methods')
    assert allow_methods is not None
    assert 'POST' in [method.strip().upper() for method in allow_methods.split(',')]
    
    # Verify Access-Control-Allow-Headers includes Authorization
    allow_headers = response.headers.get('Access-Control-Allow-Headers')
    assert allow_headers is not None
    assert 'authorization' in [header.strip().lower() for header in allow_headers.split(',')]


def test_cors_allows_all_origins_by_default(client):
    """Test that CORS allows all origins when CORS_ALLOWED_ORIGINS is not set."""
    response = client.get('/pdf-to-cbz/', headers={'Origin': 'http://example.com'})
    # Flask-CORS with default settings echoes the Origin header or returns *
    allow_origin = response.headers.get('Access-Control-Allow-Origin')
    assert allow_origin in ('*', 'http://example.com')
    
    # Test with a different origin to verify it's not restricted
    response2 = client.get('/pdf-to-cbz/', headers={'Origin': 'http://different.com'})
    allow_origin2 = response2.headers.get('Access-Control-Allow-Origin')
    assert allow_origin2 in ('*', 'http://different.com')
