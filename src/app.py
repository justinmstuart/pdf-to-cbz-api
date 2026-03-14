import os

from datetime import datetime

from flask import Flask, request
from werkzeug.utils import secure_filename

from constants.errors import Errors
from constants.response_status_codes import ResponseStatusCodes
from constants.file_ext import FileExtensions
from constants.mimetype import Mimetypes
from utils.files import save_file_to_directory, delete_directory
from utils.errors import create_error_response

app = Flask(__name__)

@app.route('/', methods=['POST'])
def pdf_to_cbz():
    # 1. Get timestamp of request
    timestamp = datetime.now().isoformat()

    # 1. Check if the request contains a file
    if "file" not in request.files:
        return create_error_response(Errors.INVALID_REQUEST_NO_FILE, ResponseStatusCodes.BAD_REQUEST)

    file = request.files["file"]
    if file.filename == '':
        return create_error_response(Errors.INVALID_REQUEST_NO_FILE, ResponseStatusCodes.BAD_REQUEST)

    # 2. Validate the file is a PDF
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext != FileExtensions.PDF or file.mimetype != Mimetypes.PDF:
        return create_error_response(Errors.INVALID_FILE_TYPE, ResponseStatusCodes.BAD_REQUEST)

    # 3. Save file to temp directory
    temp_dir = 'temp/' + timestamp
    file_path = save_file_to_directory(file, filename, temp_dir)

    # 4. Convert PDF to CBZ

    # 6. Clean up temp directory
    delete_directory(temp_dir)

    # 7. Return CBZ file as response
    return {'message': 'Hello, World!'}, ResponseStatusCodes.OK

if __name__ == '__main__':
    app.run(debug=True)
