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
