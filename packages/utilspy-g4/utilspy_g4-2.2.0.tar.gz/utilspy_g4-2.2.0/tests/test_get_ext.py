import pytest
from utilspy_g4 import get_ext


def test_1():
    path = 'test.png'
    ext = get_ext(path)
    assert ext == 'png'


def test_2():
    path = 'test.png'
    ext = get_ext(path, 0)
    assert ext == ''


def test_3():
    path = '/test/test/test.png.jpeg'
    ext = get_ext(path)
    assert ext == 'jpeg'


def test_4():
    path = 'd:\\test\\test.png.jpeg'
    ext = get_ext(path, 2)
    assert ext == 'png'


def test_5():
    path = '/foo/bar/test.txt.png.jpeg'
    ext = get_ext(path, 3)
    assert ext == 'txt'
