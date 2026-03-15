# pylint: disable=wrong-import-position
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python-utils'))

from flask import Flask
from blueprints.pdf_to_cbz_bp import pdf_to_cbz_bp
from constants.blueprints import Blueprints

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 1 GB
app.config['MAX_FORM_MEMORY_SIZE'] = 1000 * 1024 * 1024  # 1 GB

app.register_blueprint(pdf_to_cbz_bp, url_prefix=Blueprints.PDF_TO_CBZ)

if __name__ == '__main__':
    app.run(debug=True)
