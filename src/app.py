# pylint: disable=wrong-import-position
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python-utils'))

from flask import Flask
from flask_cors import CORS

from blueprints.pdf_to_cbz_bp import pdf_to_cbz_bp
from constants.blueprints import Blueprints
from constants.config import ConfigKeys
from constants.env import Env


def _get_allowed_cors_origins():
    """
    Get the list of allowed CORS origins from environment variable.
    Returns None to allow all origins (*) if not configured.
    """
    if Env.CORS_ALLOWED_ORIGINS:
        return [origin.strip() for origin in Env.CORS_ALLOWED_ORIGINS.split(',') if origin.strip()]
    return None


app = Flask(__name__)

# Configure CORS: allows all origins by default, or specific origins from environment variable.
# Set CORS_ALLOWED_ORIGINS environment variable to a comma-separated list of origins.
# Example: CORS_ALLOWED_ORIGINS='https://example.com,https://app.example.com'
allowed_origins = _get_allowed_cors_origins()
if allowed_origins:
    CORS(app, origins=allowed_origins)
else:
    CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
)

app.config[ConfigKeys.MAX_CONTENT_LENGTH] = Env.MAX_CONTENT_LENGTH
app.config[ConfigKeys.MAX_FORM_MEMORY_SIZE] = Env.MAX_FORM_MEMORY_SIZE

app.register_blueprint(pdf_to_cbz_bp, url_prefix=Blueprints.PDF_TO_CBZ)

if __name__ == '__main__':
    app.run(debug=True)
