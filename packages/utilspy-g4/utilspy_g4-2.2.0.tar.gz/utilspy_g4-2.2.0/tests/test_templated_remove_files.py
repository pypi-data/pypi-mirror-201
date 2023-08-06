import pytest
import os
from utilspy_g4 import templated_remove_files


def test_1():
    open('tests/tmp/test_1.txt', 'a').close()
    open('tests/tmp/test_2.txt', 'a').close()
    open('tests/tmp/test_1.png', 'a').close()
    open('tests/tmp/test_2.png', 'a').close()

    templated_remove_files('tests/tmp/test_1.txt')

    assert os.path.exists('tests/tmp/test_1.txt') is False
    assert os.path.exists('tests/tmp/test_2.txt')
    assert os.path.exists('tests/tmp/test_1.png')
    assert os.path.exists('tests/tmp/test_2.png')

    templated_remove_files('tests/tmp/test_*.png')

    assert os.path.exists('tests/tmp/test_2.txt')
    assert os.path.exists('tests/tmp/test_1.png') is False
    assert os.path.exists('tests/tmp/test_2.png') is False

    templated_remove_files('tests/tmp/test_*')

    assert os.path.exists('tests/tmp/test_2.txt') is False
