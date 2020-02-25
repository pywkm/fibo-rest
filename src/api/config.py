import os

DIFFICULTY = int(os.getenv("FIBO_DIFFICULTY", "200"))  # in milliseconds
SEQUENCE_ENDPOINT = "/fibo/{}"
STATUS_ENDPOINT = "/fibo/{}/status"
