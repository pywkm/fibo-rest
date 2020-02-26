from datetime import datetime, timedelta

import falcon
import freezegun
import pytest
from falcon import testing

from api.app import create_app
from api.config import DIFFICULTY, SEQUENCE_ENDPOINT, STATUS_ENDPOINT
from api.storage.abstract import Storage
from api.storage.memory import MemoryStorage
from api.types import FiboSequence


@pytest.fixture
def storage() -> Storage:
    return MemoryStorage({0: 0, 1: 1, 2: 1, 3: 2, 10: 55})


@pytest.fixture
def client(storage: Storage) -> testing.TestClient:
    app = create_app(storage)
    return testing.TestClient(app)


@pytest.fixture()
def time_to_freeze() -> datetime:
    return datetime(2020, 2, 20, 22, 00, 22)


@pytest.mark.parametrize(
    "length, expected_sequence",
    [(1, [0]), (2, [0, 1]), (3, [0, 1, 1]), (4, [0, 1, 1, 2])],
)
def test_get_sequence_for_stored_data(
    client: testing.TestClient, length: int, expected_sequence: FiboSequence
):
    expected_response = {"sequence": expected_sequence}

    response = client.simulate_get(SEQUENCE_ENDPOINT.format(length))

    assert response.status == falcon.HTTP_OK
    assert response.json == expected_response


@pytest.mark.parametrize(
    "length, missing_numbers", [(5, 1), (11, 6), (100, 95)],
)
def test_get_sequence_when_data_is_incomplete(
    client: testing.TestClient,
    time_to_freeze: datetime,
    missing_numbers: int,
    length: int,
):
    expected_status_uri = STATUS_ENDPOINT.format(length)
    expected_eta = time_to_freeze + timedelta(milliseconds=DIFFICULTY * missing_numbers)
    expected_response = {
        "sequence": None,
        "statusUri": expected_status_uri,
        "estimatedTime": str(expected_eta),
    }

    with freezegun.freeze_time(time_to_freeze):
        response = client.simulate_get(SEQUENCE_ENDPOINT.format(length))

    assert response.status == falcon.HTTP_ACCEPTED
    assert response.json == expected_response


@pytest.mark.parametrize(
    "length", [-1, 0],
)
def test_get_sequence_invalid_number_returns_bad_request_error(
    client: testing.TestClient, length: int
):
    expected_response = {
        "message": "Fibonacci sequence length must be positive integer"
    }

    response = client.simulate_get(SEQUENCE_ENDPOINT.format(length))

    assert response.status == falcon.HTTP_BAD_REQUEST
    assert response.json == expected_response


@pytest.mark.parametrize(
    "length", [1, 5, 100],
)
def test_get_status_unknown_status_returns_not_found_error(
    client: testing.TestClient, length: int
):
    expected_response = {"message": f"Calculation for {length} wasn't requested yet"}

    response = client.simulate_get(STATUS_ENDPOINT.format(length))

    assert response.status == falcon.HTTP_NOT_FOUND
    assert response.json == expected_response


@pytest.mark.parametrize(
    "length", [-1, 0],
)
def test_get_status_invalid_length_returns_bad_request_error(
    client: testing.TestClient, length: int
):
    expected_response = {
        "message": f"Fibonacci sequence length must be positive integer"
    }

    response = client.simulate_get(STATUS_ENDPOINT.format(length))

    assert response.status == falcon.HTTP_BAD_REQUEST
    assert response.json == expected_response


@pytest.mark.parametrize(
    "length, missing_numbers", [(5, 1), (11, 6), (100, 95)],
)
def test_get_status_after_requesting_status_returns_response(
    client: testing.TestClient,
    time_to_freeze: datetime,
    missing_numbers: int,
    length: int,
):
    # first request the calculation
    with freezegun.freeze_time(time_to_freeze):
        sequence_response = client.simulate_get(SEQUENCE_ENDPOINT.format(length))
    assert sequence_response.status == falcon.HTTP_ACCEPTED

    # now get status
    status_endpoint = sequence_response.json["statusUri"]
    with freezegun.freeze_time(time_to_freeze):
        status_response = client.simulate_get(status_endpoint)

    expected_eta = time_to_freeze + timedelta(milliseconds=DIFFICULTY * missing_numbers)
    expected_status_response = {
        "numbersRequired": length,
        "numbersCalculated": length - missing_numbers,
        "estimatedTime": str(expected_eta),
    }
    assert status_response.status == falcon.HTTP_OK
    assert status_response.json == expected_status_response
