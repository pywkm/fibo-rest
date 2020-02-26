#!/usr/bin/env python
from generator.config import JOB_QUEUE
from generator.fibonacci import callback
from messaging import broker

if __name__ == "__main__":
    broker.register_callback(JOB_QUEUE, callback)
    broker.start_consuming()
