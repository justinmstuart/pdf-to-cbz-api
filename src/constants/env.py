import os
from dotenv import load_dotenv

load_dotenv()

class Env:
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '1048576000'))
    MAX_FORM_MEMORY_SIZE = int(os.getenv('MAX_FORM_MEMORY_SIZE', '1048576000'))
    GUNICORN_WORKERS = int(os.getenv('GUNICORN_WORKERS', '2'))
    GUNICORN_THREADS = int(os.getenv('GUNICORN_THREADS', '4'))
    GUNICORN_TIMEOUT = int(os.getenv('GUNICORN_TIMEOUT', '120'))
    GUNICORN_WORKER_CLASS = os.getenv('GUNICORN_WORKER_CLASS', 'gthread')
    API_SECRET = os.getenv('API_SECRET', '')
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '')
