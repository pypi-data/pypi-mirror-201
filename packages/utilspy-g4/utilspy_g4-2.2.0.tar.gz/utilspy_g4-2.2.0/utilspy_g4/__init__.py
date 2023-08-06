import os
import glob
from datetime import date, datetime


def add_ext(path: str, ext: str) -> str:
    """
    Add ext to path

    :param path: Path to file
    :param ext: Added ext
    :rtype: str
    :return: Path with added ext
    """

    path_ext = os.path.splitext(path)
    return path_ext[0] + '.' + ext + path_ext[1]


def del_ext(path: str, ext_count: int = 1) -> str:
    """
    Del ext from path

    :param path: Path to file
    :param ext_count: Count of deleted ext
    :rtype: str
    :return: Path without ext
    """

    path_no_ext = path
    for _ in range(ext_count):
        path_no_ext = os.path.splitext(path_no_ext)[0]

    return path_no_ext


def templated_remove_files(template: str) -> None:
    """
    Remove files by template

    :param template: Template
    :return: None
    """

    remove_files = glob.iglob(template)

    for file in remove_files:
        os.remove(file)


def get_ext(path: str, ext_count: int = 1) -> str:
    """
    Return file extension from path

    :param path: Path to file
    :param ext_count: Count of returned extension
    :rtype: str
    :return: Extension
    """

    path_no_ext = path
    last_ext = ''
    for _ in range(ext_count):
        split_path = os.path.splitext(path_no_ext)
        path_no_ext = split_path[0]
        last_ext = split_path[1]

    if last_ext != '':
        # Del .
        last_ext = last_ext[1:]

    return last_ext


def get_files_count(files_template: str) -> int:
    """
    Get files count from filesTemplate
    :param files_template:
    :return: Files count from files_template
    """

    files = glob.iglob(files_template)

    i = 0
    for _ in files:
        i += 1

    return i


def int_to_2str(number: int) -> str:
    """
    Convert integer to 2 chars string with 0
    :param number: 1 or 2 digit integer number
    :return: 2 chars number with 0
    """

    if number < 10:
        return '0' + str(number)

    return str(number)


def to_date(date_) -> date or None:
    """
    Convert date in various formats to date format

    :param date_: date in various formats
    :return: date format
    """
    if isinstance(date_, date) or date_ is None:
        return date_
    elif isinstance(date_, str):
        template = date_template(date_)
        if template is None:
            raise TypeError()
        d = datetime.strptime(date_, template)
        return date(d.year, d.month, d.day)
    elif isinstance(date_, datetime):
        return date(date_.year, date_.month, date_.day)
    else:
        raise TypeError()


def date_template(date_: str) -> str or None:
    """
    Formats: '2006.05.30', '2006-05-30', '2006/05/30', '30.05.2006', '30-05-2006', '30/05/2006'

    :param date_: String date
    :return: date template
    """

    try:
        if date_[4] == '.' and date_[7] == '.':
            return '%Y.%m.%d'

        if date_[4] == '-' and date_[7] == '-':
            return '%Y-%m-%d'

        if date_[4] == '/' and date_[7] == '/':
            return '%Y/%m/%d'

        if date_[2] == '.' and date_[5] == '.':
            return '%d.%m.%Y'

        if date_[2] == '-' and date_[5] == '-':
            return '%d-%m-%Y'

        if date_[2] == '/' and date_[5] == '/':
            return '%d/%m/%Y'
    except IndexError:
        return None

    return None
