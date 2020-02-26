import abc
from typing import Callable


class Broker(abc.ABC):
    @abc.abstractmethod
    def register_callback(self, queue_name: str, callback: Callable) -> None:
        ...

    @abc.abstractmethod
    def start_consuming(self) -> None:
        ...

    @abc.abstractmethod
    def publish(self, queue: str, message: dict) -> None:
        ...
