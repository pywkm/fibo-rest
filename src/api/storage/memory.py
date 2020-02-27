from typing import Dict, Optional

from api.entities import RequestStatus
from api.exceptions import StatusNotFoundError
from api.storage.abstract import Storage
from api.types import Sequence


class MemoryStorage(Storage):
    """Only for test purposes. Won't work with many workers - they don't share the same memory"""

    _fibonacci_numbers: Dict[int, int] = {0: 0, 1: 1}
    _request_statuses: Dict[int, RequestStatus]

    def __init__(self, seed: Optional[Dict[int, int]] = None) -> None:
        self._request_statuses = {}
        if seed:
            self._fibonacci_numbers = seed

    @property
    def _sorted_items(self) -> Sequence:
        return sorted(self._fibonacci_numbers.items(), key=lambda item: item[0])

    def get_sequence(self, up_to_idx: int) -> Sequence:
        """First element has idx = 0, so length isn't the same as idx."""
        return [item for item in self._sorted_items if item[0] < up_to_idx]

    def get_status(self, length: int) -> RequestStatus:
        try:
            return self._request_statuses[length]
        except KeyError:
            raise StatusNotFoundError

    @property
    def highest_idx_requested(self) -> int:
        try:
            return max(self._request_statuses.keys())
        except ValueError:
            return 1  # empty dict

    def save_status(self, status: RequestStatus) -> None:
        self._request_statuses[status.length] = status
