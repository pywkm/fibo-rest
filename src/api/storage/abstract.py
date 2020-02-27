import abc

from api.entities import RequestStatus
from api.types import Sequence


class Storage(abc.ABC):
    @abc.abstractmethod
    def get_sequence(self, up_to_idx: int) -> Sequence:
        ...

    @abc.abstractmethod
    def get_status(self, length: int) -> RequestStatus:
        ...

    @property
    @abc.abstractmethod
    def highest_idx_requested(self) -> int:
        ...

    @abc.abstractmethod
    def save_status(self, status: RequestStatus) -> None:
        ...
