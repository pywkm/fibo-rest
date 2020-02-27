import json
from dataclasses import dataclass
from time import sleep
from typing import Dict, Tuple

from config import DIFFICULTY, FIBO_QUEUE, USE_MEMORY_CACHE
from messaging.abstract import Broker
from messaging.broker import RabbitMqBroker


@dataclass
class FibonacciNum:
    index: int
    value: int


MEMORY_CACHE: Dict[Tuple[int, int], FibonacciNum] = {}


def callback(_ch: str, _method: str, _properties: str, body: bytes) -> None:
    message = json.loads(body)
    calculate_up_to_index = message["length"] - 1
    first = FibonacciNum(*message["last_numbers"][0])
    second = FibonacciNum(*message["last_numbers"][1])
    publish_sequence(
        (first, second), calculate_up_to_index, RabbitMqBroker(), DIFFICULTY, USE_MEMORY_CACHE
    )


def publish_sequence(
    starting_numbers: Tuple[FibonacciNum, FibonacciNum],
    up_to_index: int,
    broker: Broker,
    difficulty: int,
    use_cache: bool,
) -> None:
    first, second = starting_numbers
    while second.index < up_to_index:
        if use_cache and (first.index, second.index) in MEMORY_CACHE:
            first, second = second, MEMORY_CACHE[(first.index, second.index)]
            continue
        next_fibo = calculate_next_fibonacci(first, second, difficulty)
        broker.publish(FIBO_QUEUE, {next_fibo.index: next_fibo.value})
        if use_cache:
            MEMORY_CACHE[(first.index, second.index)] = next_fibo
        first, second = second, next_fibo


def calculate_next_fibonacci(
    first: FibonacciNum, second: FibonacciNum, difficulty: int
) -> FibonacciNum:
    sleep(difficulty / 1000)  # difficulty given as timeout in milliseconds
    return FibonacciNum(second.index + 1, first.value + second.value)
