import json
from dataclasses import dataclass
from time import sleep

from config import DIFFICULTY, FIBO_QUEUE
from messaging.abstract import Broker
from messaging.broker import RabbitMqBroker


@dataclass
class FibonacciNum:
    index: int
    value: int


def callback(_ch, _method, _properties, body: bytes):
    message = json.loads(body)
    calculate_up_to_index = message["length"] - 1
    first = FibonacciNum(*message["last_numbers"][0])
    second = FibonacciNum(*message["last_numbers"][1])
    publish_sequence(calculate_up_to_index, first, second, RabbitMqBroker(), DIFFICULTY)


def publish_sequence(
    up_to_index: int, first: FibonacciNum, second: FibonacciNum, broker: Broker, difficulty: int
) -> None:
    while second.index < up_to_index:
        first, second = second, calculate_next_fibonacci(first, second, difficulty)
        broker.publish(FIBO_QUEUE, {second.index: second.value})


def calculate_next_fibonacci(
    first: FibonacciNum, second: FibonacciNum, difficulty: int
) -> FibonacciNum:
    sleep(difficulty / 1000)  # difficulty given as timeout in milliseconds
    return FibonacciNum(second.index + 1, first.value + second.value)
