import abc
from typing import Any, Callable


class Broker(abc.ABC):
    @abc.abstractmethod
    def register_callback(self, queue_name: str, callback: Callable[..., Any]) -> None:
        ...

    @abc.abstractmethod
    def start_consuming(self) -> None:
        ...

    @abc.abstractmethod
    def publish(self, queue_name: str, message: dict) -> None:
        ...
