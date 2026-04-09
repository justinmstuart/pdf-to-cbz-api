from constants.config import ConfigKeys


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
    response = client.get('/')
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
    # The key requirement is that Access-Control-Allow-Origin is present
    # to confirm CORS is properly configured.
    assert 'Access-Control-Allow-Origin' in response.headers
