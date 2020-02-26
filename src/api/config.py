import os

DIFFICULTY = int(os.getenv("FIBO_DIFFICULTY", "200"))  # in milliseconds
SEQUENCE_ENDPOINT = "/fibo/{}"
STATUS_ENDPOINT = "/fibo/{}/status"

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_PASS = os.getenv("DB_PASS")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
