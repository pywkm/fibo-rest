from datetime import datetime

import pytest
from mock import Mock

from api.logic import ApiLogic
from api.storage.abstract import Storage
from api.storage.memory import MemoryStorage
from messaging.abstract import Broker


@pytest.fixture
def broker_mock() -> Mock:
    return Mock(spec_set=Broker)


@pytest.fixture
def storage() -> Storage:
    return MemoryStorage({0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5, 10: 55})


@pytest.fixture
def logic(storage: Storage, broker_mock: Mock) -> ApiLogic:
    return ApiLogic(storage, broker_mock)


@pytest.fixture()
def time_to_freeze() -> datetime:
    return datetime(2020, 2, 20, 22, 00, 22)
