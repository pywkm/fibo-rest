import pytest
from api.logic import ApiLogic
from api.storage.memory import MemoryStorage


@pytest.fixture()
def logic() -> ApiLogic:
    storage = MemoryStorage({0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5})
    return ApiLogic(storage)


def test_known_sequence_is_immediately_returned(logic: ApiLogic) -> None:
    sequence, status = logic.get_sequence_status(3)
    assert sequence
    assert not status


def test_unknown_sequence_isnt_returned(logic: ApiLogic) -> None:
    sequence, status = logic.get_sequence_status(10)
    assert not sequence
    assert status
    assert status.length == 10
    assert status.calculated_items == 6
