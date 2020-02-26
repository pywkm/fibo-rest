from datetime import datetime, timedelta

from api.entities import RequestStatus, SequenceStatusDTO
from api.storage.abstract import Storage
from api.types import Sequence
from config import DIFFICULTY, JOB_QUEUE
from messaging.broker import Broker


class ApiLogic:
    def __init__(self, storage: Storage, broker: Broker) -> None:
        self._storage = storage
        self._broker = broker

    def get_sequence_with_status(self, length: int) -> SequenceStatusDTO:
        sequence = self._storage.get_sequence(length)

        if sequence and len(sequence) == length:
            return SequenceStatusDTO(sequence=[item[1] for item in sequence])

        message = {
            "length": length,
            "last_numbers": self._get_last_fibo_numbers(sequence),
        }
        self._broker.publish(JOB_QUEUE, message)

        calculated_items = len(sequence)
        now = datetime.now()
        eta = now + timedelta(milliseconds=(length - calculated_items) * DIFFICULTY)
        status = RequestStatus(length, calculated_items, now, eta)

        self._storage.save_status(status)

        return SequenceStatusDTO(status=status)

    def get_request_status(self, length: int) -> RequestStatus:
        old_status = self._storage.get_status(length)
        sequence = self._storage.get_sequence(length)
        calculated_items = len(sequence)
        new_eta = datetime.now() + timedelta(
            milliseconds=(length - calculated_items) * DIFFICULTY
        )
        new_status = RequestStatus(
            old_status.length, calculated_items, old_status.requested_at, new_eta
        )
        return new_status

    @staticmethod
    def _get_last_fibo_numbers(sequence: Sequence) -> Sequence:
        return [sequence[-2], sequence[-1]]  # dummy assumption
