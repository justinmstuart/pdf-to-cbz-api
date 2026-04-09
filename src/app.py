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

app = Flask(__name__)
# Enable CORS with default settings (allows all origins).
# For production use, consider restricting to specific origins:
# CORS(app, origins=['https://yourdomain.com'])
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
