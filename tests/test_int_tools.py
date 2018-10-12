import pytest
from pynextion.int_tools import (
    limits,
    str_int,
    assert_int_in_range,
    assert_integers_in_range,
)


def test_str_int():
    for bit_size in [8, 16, 32, 64]:
        assert str_int(True, bit_size) == "int%d" % bit_size
        assert str_int(False, bit_size) == "uint%d" % bit_size


def test_limits():
    for bit_size in [8, 16, 32, 64]:
        assert limits(False, bit_size) == (0, 2 ** bit_size - 1)
        assert limits(True, bit_size) == (-2 ** (bit_size - 1), 2 ** (bit_size - 1) - 1)


def test_assert_int_in_range_uint8():
    assert_int_in_range(0, False, 8)
    assert_int_in_range(255, False, 8)
    with pytest.raises(ValueError):
        assert_int_in_range(256, False, 8)
    with pytest.raises(ValueError):
        assert_int_in_range(-1, False, 8)


def test_assert_int_in_range_int8():
    assert_int_in_range(-128, True, 8)
    assert_int_in_range(127, True, 8)
    with pytest.raises(ValueError):
        assert_int_in_range(128, True, 8)
    with pytest.raises(ValueError):
        assert_int_in_range(-129, True, 8)


def test_assert_integers_in_range():
    assert_integers_in_range((-128, 0, 127), True, 8)  # is int8
    with pytest.raises(ValueError):
        assert_integers_in_range((-128, 0, 127), False, 8)  # is not uint8
