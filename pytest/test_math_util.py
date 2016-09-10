from pytest import raises

from math_util import power

LARGE_NUMBER = 10000000


def test_squares():
    for i in range(1, 10):
        assert i * i == power(i, 2)


def test_one_to_any_always_one():
    assert 1 == power(1, 1)
    assert 1 == power(1, 2)
    assert 1 == power(1, LARGE_NUMBER)


def test_negative_exponents():
    """ Negative exponents raise ValueError.

    They would be complicated to implement.
    """
    with raises(ValueError):
        power(1, -1)
