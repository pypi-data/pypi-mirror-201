import pytest
from utilspy_g4 import add_ext


def test_1():
    path = 'c:\\test\\test.png'
    ext = 'ext'
    new_path = add_ext(path, ext)
    assert new_path == 'c:\\test\\test.ext.png'


def test_2():
    path = '/test/test.png'
    ext = 'ext'
    new_path = add_ext(path, ext)
    assert new_path == '/test/test.ext.png'


def test_3():
    path = 'test.png'
    ext = 'ext'
    new_path = add_ext(path, ext)
    assert new_path == 'test.ext.png'


def test_4():
    path = 'c:\\test\\test'
    ext = 'ext'
    new_path = add_ext(path, ext)
    assert new_path == 'c:\\test\\test.ext'


def test_5():
    path = 'c:\\test\\test.2.png'
    ext = 'ext'
    new_path = add_ext(path, ext)
    assert new_path == 'c:\\test\\test.2.ext.png'
