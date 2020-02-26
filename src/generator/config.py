import os

DIFFICULTY = int(os.getenv("FIBO_DIFFICULTY", "200"))  # in milliseconds

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
JOB_QUEUE = os.getenv("JOB_QUEUE", "job_queue")
FIBO_QUEUE = os.getenv("FIBO_QUEUE", "fibo_queue")
