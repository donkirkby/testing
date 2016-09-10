from unittest import TestCase

from file_util import first_byte


class FileUtilTest(TestCase):
    def setUp(self):
        self.zero_file = open('/dev/zero', 'rb')
        self.addCleanup(self.zero_file.close)

    def test_first_byte(self):
        self.assertEqual(0, first_byte(self.zero_file))
