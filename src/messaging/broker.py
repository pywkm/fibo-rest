import json
from typing import Callable

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError

from config import FIBO_QUEUE, JOB_QUEUE, RABBITMQ_HOST
from messaging.abstract import Broker


class RabbitMqBroker(Broker):
    """Singleton"""

    __instance = None
    _connection: pika.BlockingConnection = None
    _channel: BlockingChannel = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self._parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST, connection_attempts=5, retry_delay=3
        )
        self.connect()

    def connect(self):
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        self._declare_queues()

    def register_callback(self, queue_name: str, callback: Callable) -> None:
        self._channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

    def start_consuming(self) -> None:
        self._channel.start_consuming()

    def publish(self, queue_name: str, message: dict) -> None:
        try:
            self._channel.basic_publish(
                exchange="", routing_key=queue_name, body=json.dumps(message)
            )
        except AMQPConnectionError:
            self.connect()
            self.publish(queue_name, message)

    def _declare_queues(self):
        self._channel.queue_declare(queue=JOB_QUEUE)
        self._channel.queue_declare(queue=FIBO_QUEUE)
