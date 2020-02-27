from datetime import datetime

import pytest

from api.entities import RequestStatus
from api.exceptions import StatusNotFoundError
from api.storage.abstract import Storage
from api.types import Sequence


@pytest.mark.parametrize(
    "length, expected_sequence",
    [
        (-1, []),
        (0, []),
        (1, [(0, 0)]),
        (2, [(0, 0), (1, 1)]),
        (3, [(0, 0), (1, 1), (2, 1)]),
        (5, [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3)]),
        (13, [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (10, 55)]),
        (42, [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (10, 55)]),
    ],
)
def test_get_sequence(storage: Storage, length: int, expected_sequence: Sequence) -> None:
    assert storage.get_sequence(length) == expected_sequence


def test_get_status_from_empty_storage(storage: Storage) -> None:
    with pytest.raises(StatusNotFoundError):
        storage.get_status(4)


def test_saving_status_adds_status_only_for_that_length(storage: Storage) -> None:
    length = 5
    storage.save_status(RequestStatus(length, 3, datetime.now(), datetime.now()))
    assert storage.get_status(length)
    with pytest.raises(StatusNotFoundError):
        storage.get_status(length + 1)
