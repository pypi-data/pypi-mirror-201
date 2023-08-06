import pytest
from utilspy_g4 import del_ext


def test_1():
    path = 'test.png'
    new_path = del_ext(path)
    assert new_path == 'test'


def test_2():
    path = '/test/test.jpeg'
    new_path = del_ext(path)
    assert new_path == '/test/test'


def test_3():
    path = 'c:\\test\\test.p'
    new_path = del_ext(path)
    assert new_path == 'c:\\test\\test'


def test_4():
    path = 'd:\\test\\test.png.jpeg'
    new_path = del_ext(path)
    assert new_path == 'd:\\test\\test.png'


def test_5():
    path = 'd:\\test\\test.png.jpeg'
    new_path = del_ext(path, 2)
    assert new_path == 'd:\\test\\test'


def test_6():
    path = '/test/test.png.jpeg'
    new_path = del_ext(path, 2)
    assert new_path == '/test/test'


def test_7():
    path = 'test.jpeg.png'
    new_path = del_ext(path, 2)
    assert new_path == 'test'
