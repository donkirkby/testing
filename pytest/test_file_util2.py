import pytest

from file_util import first_byte


@pytest.fixture()
def zero_file(request):
    with open('/dev/zero', 'rb') as f:
        yield f


def test_first_byte(zero_file):
    assert 0 == first_byte(zero_file)
