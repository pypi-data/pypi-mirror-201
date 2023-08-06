import pytest

from utilspy_g4 import get_files_count


def test_1():
    assert get_files_count('tests/test_getFilesCount/foo_?.txt') == 3

    assert get_files_count('tests/test_getFilesCount/bar_*.txt') == 2

    assert get_files_count('tests/test_getFilesCount/foo.txt') == 1

    assert get_files_count('tests/test_getFilesCount/test_?.txt') == 0

    assert get_files_count('tests/test_getFilesCount_test/foo_?.txt') == 0
