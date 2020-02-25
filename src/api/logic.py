from datetime import datetime, timedelta
from typing import Optional, Tuple

from api.entities import RequestStatus
from api.storage.abstract import Storage
from api.types import FiboSequence


class ApiLogic:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def get_sequence_status(
        self, length: int
    ) -> Tuple[Optional[FiboSequence], Optional[RequestStatus]]:

        sequence = self._storage.get_sequence(length)

        if sequence:
            return sequence, None

        # send calculation request to rabbitmq

        last_element = self._storage.get_last_element(length)
        status = RequestStatus(
            length,
            last_element,
            datetime.now(),
            datetime.now() + timedelta(days=length),
        )

        self._storage.save_status(status)

        return None, status

    def get_status(self, length: int) -> RequestStatus:
        return self._storage.get_status(length)

    def _update_status(self, length: int) -> RequestStatus:
        pass
