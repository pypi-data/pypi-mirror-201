import pytest

from utilspy_g4 import date_template


def test_1():
    assert date_template('2006.05.30') == '%Y.%m.%d'

    assert date_template('2016-12-23') == '%Y-%m-%d'

    assert date_template('1934/02/03') == '%Y/%m/%d'

    assert date_template('28.10.1990') == '%d.%m.%Y'

    assert date_template('08-01-1888') == '%d-%m-%Y'

    assert date_template('21/12/2120') == '%d/%m/%Y'


def test_2():
    assert date_template('1/2/22') is None

    assert date_template('no date') is None

    assert date_template('') is None
