import os

DIFFICULTY = int(os.getenv("FIBO_DIFFICULTY", "200"))  # in milliseconds
REAL_DIFFICULTY = DIFFICULTY + 10  # let's add some time for better ETA estimation
SEQUENCE_ENDPOINT = "/fibo/{}"
STATUS_ENDPOINT = "/fibo/{}/status"

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_PASS = os.getenv("DB_PASS")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
JOB_QUEUE = os.getenv("JOB_QUEUE", "job_queue")
FIBO_QUEUE = os.getenv("FIBO_QUEUE", "fibo_queue")

USE_MEMORY_CACHE = os.getenv("GENERATOR_CACHE", "off").lower() == "on"

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
