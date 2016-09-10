from nose.tools import assert_equal, assert_raises
from math_util import power

LARGE_NUMBER = 10000000


def test_squares():
    for i in range(1, 10):
        assert_equal(i * i, power(i, 2))


def test_one_to_any_always_one():
    assert_equal(1, power(1, 1))
    assert_equal(1, power(1, 2))
    assert_equal(
        1,
        power(1, LARGE_NUMBER))


def test_negative_exponents():
    """ Negative exponents raise ValueError.

    They would be complicated to implement.
    """
    with assert_raises(ValueError):
        power(1, -1)
