import pytest

from include.inspect_values import is_present
import pytest

@pytest.mark.parametrize(
    "value,expected", [
        ("hello", True),
        (123, True),
        ([1, 2, 3], True),
        ({"key": "value"}, True),
        (0, False),
        ("", False),
        ("   ", False),
        (".", False),
        ([], False),
        ({}, False),
        (None, False),
        (" . ", False),
        (False, False)
    ]
)
def test_is_present(value, expected):
    assert is_present(value) == expected
