import os

PORT = os.getenv("GUNICORN_PORT")
WORKERS = os.getenv("GUNICORN_WORKERS", "4")

# pylint: disable=C0103
bind = f"0.0.0.0:{PORT}"
workers = int(WORKERS)
timeout = 30
worker_connections = 1000
