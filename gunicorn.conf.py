from src.constants.env import Env

bind = "0.0.0.0:8000"
workers = Env.GUNICORN_WORKERS
worker_class = Env.GUNICORN_WORKER_CLASS
threads = Env.GUNICORN_THREADS
timeout = Env.GUNICORN_TIMEOUT
accesslog = "-"
errorlog = "-"
chdir = "src"
