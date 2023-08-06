import pytest

from datetime import date, datetime
from utilspy_g4 import to_date


def test_1():
    assert to_date(None) is None

    d = date(2010, 1, 2)
    assert to_date(d) == d


def test_2():
    dt = datetime(2010, 1, 2)
    d = to_date(dt)

    assert d.day == 2
    assert d.month == 1
    assert d.year == 2010


def test_3():
    str_date = '2006.05.30'
    d = to_date(str_date)

    assert d.day == 30
    assert d.month == 5
    assert d.year == 2006

    str_date = '2016-12-23'
    d = to_date(str_date)

    assert d.day == 23
    assert d.month == 12
    assert d.year == 2016

    str_date = '1934/02/03'
    d = to_date(str_date)

    assert d.day == 3
    assert d.month == 2
    assert d.year == 1934

    str_date = '28.10.1990'
    d = to_date(str_date)

    assert d.day == 28
    assert d.month == 10
    assert d.year == 1990

    str_date = '08-01-1888'
    d = to_date(str_date)

    assert d.day == 8
    assert d.month == 1
    assert d.year == 1888

    str_date = '21/12/2120'
    d = to_date(str_date)

    assert d.day == 21
    assert d.month == 12
    assert d.year == 2120


def test_4():
    with pytest.raises(TypeError):
        to_date(123)

    with pytest.raises(TypeError):
        to_date('no date')

    str_date = '32/30/2120'
    with pytest.raises(ValueError):
        to_date(str_date)

    with pytest.raises(TypeError):
        to_date('')
