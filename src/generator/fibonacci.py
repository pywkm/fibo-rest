import json
from time import sleep

from config import FIBO_QUEUE
from messaging import broker


def callback(_ch, _method, _properties, body):
    message = json.loads(body)
    calculate(message["length"], message["last_numbers"])


def calculate(length, last_numbers):
    sleep(3)
    broker.publish(FIBO_QUEUE, {length: last_numbers})
