import json

import psycopg2

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from ingest import logger


def callback(_ch: str, _method: str, _properties: str, body: bytes) -> None:
    message = json.loads(body)
    ((index, value),) = message.items()
    insert_fibo_into_db(index, value)


def insert_fibo_into_db(index: int, value: int) -> None:
    logger.info(f"--------- RECEIVED {index, value} ----------------")
    connection = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    cursor = connection.cursor()
    cursor.execute(
        """
    INSERT INTO fibonacci_numbers (index, value)
    VALUES (%s, %s)
    ON CONFLICT ON CONSTRAINT fibonacci_numbers_pkey
    DO NOTHING;
    """,
        (index, value),
    )
    connection.commit()
    cursor.close()
    connection.close()
