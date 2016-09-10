import pytest
from StringIO import StringIO

from file_util import first_byte


@pytest.fixture(params=['\00\00\00', '\00\01\01'])
def zero_file(request):
    return StringIO(request.param)


def test_first_byte(zero_file):
    assert 0 == first_byte(zero_file)
