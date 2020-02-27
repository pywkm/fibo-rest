from typing import Dict, List

import mock
import pytest

from config import FIBO_QUEUE
from generator.fibonacci import FibonacciNum, calculate_next_fibonacci, publish_sequence


@pytest.mark.parametrize(
    "first_fibo, second_fibo, expected_next_fibo",
    [
        (FibonacciNum(0, 0), FibonacciNum(1, 1), FibonacciNum(2, 1)),
        (FibonacciNum(2, 1), FibonacciNum(3, 2), FibonacciNum(4, 3)),
        (FibonacciNum(10, 55), FibonacciNum(11, 89), FibonacciNum(12, 144)),
    ],
)
def test_calculating_next_fibonacci_numbers(
    first_fibo: FibonacciNum, second_fibo: FibonacciNum, expected_next_fibo: FibonacciNum
) -> None:
    assert calculate_next_fibonacci(first_fibo, second_fibo, difficulty=0) == expected_next_fibo


@pytest.mark.parametrize(
    "first_fibo, second_fibo, up_to_index, expected_sequence",
    [
        (FibonacciNum(0, 0), FibonacciNum(1, 1), 1, []),
        (FibonacciNum(0, 0), FibonacciNum(1, 1), 3, [{2: 1}, {3: 2}]),
        (FibonacciNum(2, 1), FibonacciNum(3, 2), 4, [{4: 3}]),
        (FibonacciNum(0, 0), FibonacciNum(1, 1), 4, []),  # cached
        (FibonacciNum(10, 55), FibonacciNum(11, 89), 14, [{12: 144}, {13: 233}, {14: 377}]),
        (FibonacciNum(10, 55), FibonacciNum(11, 89), 16, [{15: 610}, {16: 987}]),  # cached
    ],
)
def test_publishing_sequence_with_cache(
    broker_mock: mock.Mock,
    first_fibo: FibonacciNum,
    second_fibo: FibonacciNum,
    up_to_index: int,
    expected_sequence: List[Dict[int, int]],
) -> None:
    publish_sequence(
        (first_fibo, second_fibo), up_to_index, broker_mock, difficulty=0, use_cache=True
    )
    assert_called_with_values(broker_mock, expected_sequence)


@pytest.mark.parametrize(
    "first_fibo, second_fibo, up_to_index, expected_sequence",
    [
        (FibonacciNum(0, 0), FibonacciNum(1, 1), 1, []),
        (FibonacciNum(0, 0), FibonacciNum(1, 1), 3, [{2: 1}, {3: 2}]),
        (FibonacciNum(2, 1), FibonacciNum(3, 2), 4, [{4: 3}]),
        (FibonacciNum(0, 0), FibonacciNum(1, 1), 4, [{2: 1}, {3: 2}, {4: 3}]),
        (FibonacciNum(10, 55), FibonacciNum(11, 89), 14, [{12: 144}, {13: 233}, {14: 377}]),
        (
            FibonacciNum(10, 55),
            FibonacciNum(11, 89),
            16,
            [{12: 144}, {13: 233}, {14: 377}, {15: 610}, {16: 987}],
        ),
    ],
)
def test_publishing_sequence_without_cache(
    broker_mock: mock.Mock,
    first_fibo: FibonacciNum,
    second_fibo: FibonacciNum,
    up_to_index: int,
    expected_sequence: List[Dict[int, int]],
) -> None:
    publish_sequence(
        (first_fibo, second_fibo), up_to_index, broker_mock, difficulty=0, use_cache=False
    )
    assert_called_with_values(broker_mock, expected_sequence)


def assert_called_with_values(
    broker_mock: mock.Mock, expected_sequence: List[Dict[int, int]]
) -> None:
    expected_calls = [mock.call(FIBO_QUEUE, call) for call in expected_sequence]
    if expected_calls:
        assert broker_mock.publish.call_count == len(expected_calls)
        broker_mock.publish.assert_has_calls(expected_calls)
    else:
        broker_mock.publish.assert_not_called()
