import abc
from typing import Optional

from api.entities import RequestStatus
from api.types import FiboSequence


class Storage(abc.ABC):
    @abc.abstractmethod
    def get_sequence(self, length: int) -> Optional[FiboSequence]:
        ...

    @abc.abstractmethod
    def get_status(self, length: int) -> RequestStatus:
        ...

    @abc.abstractmethod
    def save_status(self, status: RequestStatus) -> None:
        ...
