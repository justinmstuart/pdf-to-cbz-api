import os
import sys
from unittest.mock import MagicMock

# Mock the python-utils submodule before any application imports
sys.modules['scripts'] = MagicMock()
sys.modules['scripts.pdf_to_cbz'] = MagicMock()

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest  # noqa: E402
from app import app as flask_app  # noqa: E402


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
