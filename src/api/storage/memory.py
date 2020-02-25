from datetime import datetime, timedelta
from typing import Dict, Optional

from api.entities import RequestStatus
from api.exceptions import StatusNotFoundError
from api.storage.abstract import Storage
from api.types import FiboSequence


class MemoryStorage(Storage):
    _calculated_numbers: Dict[int, int] = {0: 0, 1: 1}

    def __init__(self, seed: Optional[Dict[int, int]] = None) -> None:
        if seed:
            self._calculated_numbers = seed

    def get_sequence(self, length: int) -> Optional[FiboSequence]:
        if length > len(self._calculated_numbers) or length < 1:
            return None
        elements = sorted(self._calculated_numbers.items(), key=lambda elt: elt[0])[
            :length
        ]
        print(elements)
        if elements[-1][0] != length - 1:
            return None
        return [elt[1] for elt in elements]

    def get_last_element(self, length: int) -> int:
        elements = sorted(self._calculated_numbers.items(), key=lambda elt: elt[0])[
            :length
        ]
        return elements[-1][1]

    def get_status(self, length: int) -> RequestStatus:
        if length >= 10:
            raise StatusNotFoundError
        return RequestStatus(
            length, 5, datetime.now(), datetime.now() + timedelta(seconds=3)
        )

    def save_status(self, status: RequestStatus) -> None:
        pass
