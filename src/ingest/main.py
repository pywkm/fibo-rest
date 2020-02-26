#!/usr/bin/env python
from ingest.config import FIBO_QUEUE
from ingest.db import callback
from messaging import broker

if __name__ == "__main__":
    broker.register_callback(FIBO_QUEUE, callback)
    broker.start_consuming()
