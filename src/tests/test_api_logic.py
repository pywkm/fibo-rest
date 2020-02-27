from datetime import timedelta
from typing import List
from unittest import mock

import pytest
from mock import Mock

from api.entities import SequenceStatusDTO
from api.exceptions import StatusNotFoundError
from api.logic import ApiLogic
from config import JOB_QUEUE, REAL_DIFFICULTY


def test_known_sequence_is_immediately_returned(logic: ApiLogic) -> None:
    dto: SequenceStatusDTO = logic.get_sequence_with_status(4)
    assert dto.sequence
    assert dto.sequence == [0, 1, 1, 2]
    assert not dto.status


def test_unknown_sequence_isnt_returned(logic: ApiLogic) -> None:
    dto: SequenceStatusDTO = logic.get_sequence_with_status(7)
    assert not dto.sequence
    assert dto.status
    assert dto.status.length == 7
    assert dto.status.calculated_numbers == 6


def test_having_last_item_of_fibo_sequence_doesnt_mean_sequence_is_complete(
    logic: ApiLogic,
) -> None:
    dto: SequenceStatusDTO = logic.get_sequence_with_status(11)
    assert not dto.sequence
    assert dto.status
    assert dto.status.length == 11
    assert dto.status.calculated_numbers == 7


def test_getting_status_of_not_requested_sequence_raises_an_error(logic: ApiLogic) -> None:
    with pytest.raises(StatusNotFoundError):
        logic.get_request_status(13)


def test_requesting_sequence_and_getting_its_status(logic: ApiLogic) -> None:
    logic.get_sequence_with_status(15)
    status = logic.get_request_status(15)
    assert status.length == 15
    assert status.calculated_numbers == 7


def test_estimated_time_is_proportional_to_missing_numbers(logic: ApiLogic) -> None:
    dto: SequenceStatusDTO = logic.get_sequence_with_status(11)
    assert dto.status
    missing_numbers = dto.status.length - dto.status.calculated_numbers
    eta_milliseconds_diff = missing_numbers * REAL_DIFFICULTY
    assert dto.status.eta == dto.status.requested_at + timedelta(milliseconds=eta_milliseconds_diff)


def test_eta_is_longer_with_every_status_check_if_no_new_items_occurs(logic: ApiLogic) -> None:
    dto: SequenceStatusDTO = logic.get_sequence_with_status(12)
    assert dto.status
    original_requested_at = dto.status.requested_at
    original_eta = dto.status.eta

    status = logic.get_request_status(12)
    assert status.requested_at == original_requested_at
    # after a moment still the same calculated items, so eta should be a little later
    assert status.eta > original_eta


def test_eta_is_shorter_when_there_are_new_items_added(logic: ApiLogic) -> None:
    dto: SequenceStatusDTO = logic.get_sequence_with_status(12)
    assert dto.status
    original_requested_at = dto.status.requested_at
    original_eta = dto.status.eta

    # simulate adding new items to storage, access to protected members, so disabling linters
    logic._storage._fibonacci_numbers.update({6: 8})  # type: ignore  # pylint: disable=W0212

    status = logic.get_request_status(12)
    assert status.requested_at == original_requested_at
    # after a moment one more calculated items, so eta should be a little earlier
    assert status.eta < original_eta


def test_message_is_sent_to_broker(logic: ApiLogic, broker_mock: Mock) -> None:
    length = 12
    logic.get_sequence_with_status(length)
    logic.get_sequence_with_status(length + 1)
    expected_message_1 = {"length": length, "last_numbers": [(4, 3), (5, 5)]}
    expected_message_2 = {"length": length + 1, "last_numbers": [(4, 3), (5, 5)]}
    assert_called_with_values(broker_mock, [expected_message_1, expected_message_2])


def assert_called_with_values(broker_mock: mock.Mock, expected_messages: List[dict]) -> None:
    expected_calls = [mock.call(JOB_QUEUE, call) for call in expected_messages]
    if expected_calls:
        assert broker_mock.publish.call_count == len(expected_calls)
        broker_mock.publish.assert_has_calls(expected_calls)
    else:
        broker_mock.publish.assert_not_called()


def test_message_isnt_sent_to_broker_again_if_already_equal_or_higher_idx_requested(
    logic: ApiLogic, broker_mock: Mock
) -> None:
    length = 12
    expected_queue = JOB_QUEUE
    expected_message = {"length": length, "last_numbers": [(4, 3), (5, 5)]}

    # First request
    logic.get_sequence_with_status(length)

    # Second request
    logic.get_sequence_with_status(length)

    # Third request
    logic.get_sequence_with_status(length - 1)

    # But only called once
    broker_mock.publish.assert_called_once_with(expected_queue, expected_message)
