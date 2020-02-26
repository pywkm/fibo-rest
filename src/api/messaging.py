import abc
import json

import pika

from config import RABBITMQ_HOST


class Broker(abc.ABC):
    @abc.abstractmethod
    def send(self, queue: str, message: dict) -> None:
        ...


class RabbitMqBroker(Broker):
    def send(self, queue: str, message: dict) -> None:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                content_type="application/json", delivery_mode=2,
            ),
        )
        connection.close()
