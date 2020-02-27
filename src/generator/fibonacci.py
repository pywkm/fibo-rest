import json
from dataclasses import dataclass
from time import sleep

from config import DIFFICULTY, FIBO_QUEUE
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
    continue_sequence(calculate_up_to_index, first, second)


def continue_sequence(up_to_index: int, first: FibonacciNum, second: FibonacciNum) -> None:
    while second.index < up_to_index:
        first, second = second, calculate_next_fibonacci(first, second, DIFFICULTY)
        RabbitMqBroker().publish(FIBO_QUEUE, {second.index: second.value})


def calculate_next_fibonacci(
    first: FibonacciNum, second: FibonacciNum, difficulty: int = 0
) -> FibonacciNum:
    sleep(difficulty / 1000)  # difficulty given in milliseconds
    return FibonacciNum(second.index + 1, first.value + second.value)
