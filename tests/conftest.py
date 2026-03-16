import os
import sys
import types

import pytest

# Stub the python-utils submodule before any application imports.
# Using real ModuleType objects (not MagicMock) so that only the expected
# symbol is defined — any unexpected import from the submodule fails loudly.
_scripts_mod = types.ModuleType('scripts')
_pdf_to_cbz_mod = types.ModuleType('scripts.pdf_to_cbz')


def _process_pdf_files(*_args, **_kwargs):
    pass


_pdf_to_cbz_mod.process_pdf_files = _process_pdf_files
sys.modules['scripts'] = _scripts_mod
sys.modules['scripts.pdf_to_cbz'] = _pdf_to_cbz_mod

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app as flask_app  # pylint: disable=wrong-import-position


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
