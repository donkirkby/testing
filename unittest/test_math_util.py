from logging import basicConfig, CRITICAL, WARN
from unittest2 import TestCase

from math_util import power

LARGE_NUMBER = 10000000


class PowerTest(TestCase):
    def setUp(self):
        self.longMessage = True

    def test_squares(self):
        for i in range(1, 10):
            self.assertEqual(i * i, power(i, 2), '{} squared'.format(i))

    def test_one_to_any_always_one(self):
        basicConfig(level=CRITICAL)
        self.assertEqual(1, power(1, 1))
        self.assertEqual(1, power(1, 2))
        self.assertEqual(
            1,
            power(1, LARGE_NUMBER))

    def test_negative_exponents(self):
        """ Negative exponents raise ValueError.

        They would be complicated to implement.
        """
        with self.assertRaises(ValueError):
            power(1, -1)

    def test_warning(self):
        basicConfig(level=CRITICAL)
        expected = [
            'WARNING:root:Large power used.']

        with self.assertLogs(level=WARN) as ctx:
            power(1, LARGE_NUMBER)
        self.assertEqual(expected, ctx.output)
