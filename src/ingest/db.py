import json

from ingest import logger


def callback(_ch, _method, _properties, body):
    message = json.loads(body)
    put_in_db(message)


def put_in_db(message):
    logger.info(f"--------- RECEIVED {message} ----------------")
