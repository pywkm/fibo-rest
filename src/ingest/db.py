import json

import psycopg2

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from ingest import logger

SQL = """
INSERT INTO fibonacci_numbers (index, value)
VALUES (%s, %s)
ON CONFLICT ON CONSTRAINT fibonacci_numbers_pkey
DO NOTHING;
"""


def callback(_ch: str, _method: str, _properties: str, body: bytes) -> None:
    message = json.loads(body)
    logger.debug("Received message: %s", message)
    ((index, value),) = message.items()
    insert_fibo_into_db(index, value)


def insert_fibo_into_db(index: int, value: int) -> None:
    logger.debug("Pair to save in DB: (%s, %s)", index, value)
    connection = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL, (index, value))
    # Exiting context manager does not close connection. Only commits transaction.
    connection.close()
