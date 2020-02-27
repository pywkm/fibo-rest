#!/usr/bin/env python
from config import JOB_QUEUE
from generator.fibonacci import callback
from messaging.broker import RabbitMqBroker

if __name__ == "__main__":
    broker = RabbitMqBroker()
    broker.register_callback(JOB_QUEUE, callback)
    broker.start_consuming()
