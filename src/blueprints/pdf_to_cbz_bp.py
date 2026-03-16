import logging
import os
from datetime import datetime

from flask import Blueprint, request, send_file
from werkzeug.utils import secure_filename
from scripts.pdf_to_cbz import process_pdf_files

from constants.request_methods import RequestMethods
from constants.blueprints import Blueprints
from constants.errors import Errors
from constants.file_ext import FileExtensions
from constants.mimetype import Mimetypes
from constants.response_status_codes import ResponseStatusCodes

from utils.errors import create_error_response
from utils.files import save_file_to_directory, delete_directory

logger = logging.getLogger(__name__)

class Routes:
    ROOT = '/'

pdf_to_cbz_bp = Blueprint(Blueprints.PDF_TO_CBZ, __name__)

@pdf_to_cbz_bp.route(Routes.ROOT, methods=[RequestMethods.POST])
def pdf_to_cbz():
    # 1. Get timestamp of request
    timestamp = datetime.now().isoformat()
    logger.info('1. Request received at %s', timestamp)

    # 2. Check if the request contains a file
    logger.info('2. Checking request for file - files: %s, content_type: %s', request.files, request.content_type)
    if 'file' not in request.files:
        logger.warning('2. No file in request')
        return create_error_response(
            Errors.INVALID_REQUEST_NO_FILE,
            ResponseStatusCodes.BAD_REQUEST
        )

    file = request.files['file']
    if file.filename == '' or file.filename is None:
        logger.warning('2. File has no filename')
        return create_error_response(
            Errors.INVALID_REQUEST_NO_FILE,
            ResponseStatusCodes.BAD_REQUEST
        )

    # 3. Validate the file is a PDF
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    logger.info('3. Validating file - filename: %s, ext: %s, mimetype: %s', filename, ext, file.mimetype)
    if ext != FileExtensions.PDF or file.mimetype != Mimetypes.PDF:
        logger.warning('3. Invalid file type - ext: %s, mimetype: %s', ext, file.mimetype)
        return create_error_response(
            Errors.INVALID_FILE_TYPE,
            ResponseStatusCodes.BAD_REQUEST
        )

    # 4. Save file to temp directory
    temp_dir = 'temp/' + timestamp
    logger.info('4. Saving file to temp directory: %s', temp_dir)
    file_path = save_file_to_directory(file, filename, temp_dir)

    # 5. Convert PDF to CBZ
    logger.info('5. Converting PDF to CBZ: %s', file_path)
    try:
        process_pdf_files(temp_dir)
    except Exception as e:
        logger.error('5. Conversion failed: %s', e)
        return create_error_response(
            str(e),
            ResponseStatusCodes.INTERNAL_SERVER_ERROR
        )

    # 6. Get cbz file
    cbz_file_path = os.path.splitext(file_path)[0] + '.cbz'
    logger.info('6. Looking for CBZ file: %s', cbz_file_path)
    if not os.path.exists(cbz_file_path):
        logger.error('6. CBZ file not found: %s', cbz_file_path)
        return create_error_response(
            Errors.CONVERSION_FAILED,
            ResponseStatusCodes.INTERNAL_SERVER_ERROR
        )

    # 7. Get file
    cbz_filename = os.path.basename(cbz_file_path)
    logger.info('7. CBZ filename: %s', cbz_filename)

    # 8. Create response with CBZ file
    logger.info('8. Creating response with CBZ file: %s', cbz_file_path)
    response = send_file(
        os.path.abspath(cbz_file_path),
        mimetype=Mimetypes.CBZ,
        as_attachment=True,
        download_name=cbz_filename
    )

    # 9. Clean up temp directory
    logger.info('9. Cleaning up temp directory: %s', temp_dir)
    delete_directory(temp_dir)

    # 10. Return CBZ file as response
    logger.info('10. Returning CBZ file response')
    return response
