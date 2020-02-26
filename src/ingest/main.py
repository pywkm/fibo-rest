#!/usr/bin/env python
from config import FIBO_QUEUE
from ingest.db import callback
from messaging.broker import RabbitMqBroker

if __name__ == "__main__":
    broker = RabbitMqBroker()
    broker.register_callback(FIBO_QUEUE, callback)
    broker.start_consuming()
