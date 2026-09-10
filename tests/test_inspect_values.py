import pytest

from include.inspect_values import is_present
from include.inspect_values import join_present

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

@pytest.mark.parametrize(
    "value,expected", [
        (("hello", "world"), "hello, world"),
        ((123, 456), "123, 456"),
        (([1, 2], [3, 4]), "[1, 2], [3, 4]"),
        (({"key": "value"}, {"another": "item"}), "{'key': 'value'}, {'another': 'item'}"),
        ((0, "", None), ""),
        (("", "   ", "."), ""),
        (([], {}, None), ""),
        ((None, None), ""),
        (("hello", None, "world"), "hello, world"),
        (("   ", "test", "."), "test"),
        (("Paris", "Île-de-France", None, ".", "."), "Paris, Île-de-France"),
        ((None, None, ".", ".", "Italy"), "Italy")
    ]   
)
def test_join_present(value, expected):
    assert join_present(*value) == expected
