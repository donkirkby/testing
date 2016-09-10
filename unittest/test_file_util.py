from unittest import TestCase
from StringIO import StringIO

from file_util import first_byte


class FileUtilTest(TestCase):
    def test_first_byte(self):
        zero_file = StringIO('\00\00\00')

        self.assertEqual(0, first_byte(zero_file))
