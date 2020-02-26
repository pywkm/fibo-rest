import json
from typing import Callable

import pika
from generator.config import FIBO_QUEUE, JOB_QUEUE, RABBITMQ_HOST


class Broker:
    def __init__(self):
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST, connection_attempts=5, retry_delay=3
        )
        connection = pika.BlockingConnection(parameters)
        self._channel = connection.channel()
        self._declare_queues()

    def register_callback(self, queue_name: str, callback: Callable) -> None:
        self._channel.basic_consume(
            queue=queue_name, auto_ack=True, on_message_callback=callback
        )

    def start_consuming(self):
        self._channel.start_consuming()

    def publish(self, queue_name: str, message: dict) -> None:
        self._channel.basic_publish(
            exchange="", routing_key=queue_name, body=json.dumps(message)
        )

    def _declare_queues(self):
        self._channel.queue_declare(queue=JOB_QUEUE)
        self._channel.queue_declare(queue=FIBO_QUEUE)


broker = Broker()
