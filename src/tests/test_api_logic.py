from datetime import timedelta

import pytest

from api.entities import SequenceStatusDTO
from api.exceptions import StatusNotFoundError
from api.logic import ApiLogic
from config import DIFFICULTY


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


def test_getting_status_of_not_requested_sequence_raises_an_error(logic: ApiLogic):
    with pytest.raises(StatusNotFoundError):
        logic.get_request_status(13)


def test_requesting_sequence_and_getting_its_status(logic: ApiLogic):
    logic.get_sequence_with_status(15)
    status = logic.get_request_status(15)
    assert status.length == 15
    assert status.calculated_numbers == 7


def test_estimated_time_is_proportional_to_missing_numbers(logic: ApiLogic):
    dto: SequenceStatusDTO = logic.get_sequence_with_status(11)
    assert dto.status
    missing_numbers = dto.status.length - dto.status.calculated_numbers
    eta_milliseconds_diff = missing_numbers * DIFFICULTY
    assert dto.status.eta == dto.status.requested_at + timedelta(
        milliseconds=eta_milliseconds_diff
    )


def test_eta_is_longer_with_every_status_check_if_no_new_items_occurs(logic: ApiLogic):
    dto: SequenceStatusDTO = logic.get_sequence_with_status(12)
    assert dto.status
    original_requested_at = dto.status.requested_at
    original_eta = dto.status.eta

    status = logic.get_request_status(12)
    assert status.requested_at == original_requested_at
    # after a moment still the same calculated items, so eta should be a little later
    assert status.eta > original_eta


def test_eta_is_shorter_when_there_are_new_items_added(logic: ApiLogic):
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
