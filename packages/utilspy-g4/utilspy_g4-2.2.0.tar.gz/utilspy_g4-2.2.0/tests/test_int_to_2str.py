import pytest
from utilspy_g4 import int_to_2str


def test_1():
    assert int_to_2str(2) == '02'

    assert int_to_2str(0) == '00'

    assert int_to_2str(34) == '34'

    assert int_to_2str(10) == '10'
