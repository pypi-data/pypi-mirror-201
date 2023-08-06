"""
    ==============
    Text Util
    ==============

    외부에서 온 문자열에서 다음과 같은 처리를 합니다.


    1. 문자열에서 모두 xxxx를 제거 후 반환 합니다.

    .. code-block::

        def remove_xxxx(text: str, default: Optional[str] = None):
            ...

    2. 문자열 처음과 마지막 에서만 제거 후 반환 합니다.

    .. code-block::

        def strip_xxxx(text: str, default: Optional[str] = None):
            ...

    3. 문자열에서 xxxx 형태를 추출하여 반환 합니다.

    .. code-block::

        def convert_xxxx(text: str, default: Optional[str] = None):
            ...

    4. 문자열에서 xxx를 추출하여 반환 합니다.

    .. code-block::

        def extract_xxxx(text: str, default: Optional[str] = None):
            ...

"""
import re
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union

from gpp.datetimes import dt

HANGUL_PATTERN = re.compile('[가-힣|ㄱ-ㅎ|ㅏ-ㅣ]+')
TRIM_CHARS_PATTERN = re.compile(r'(\s*)')
NUMBER_PATTERN = re.compile(r'[^0-9\-\.]')

WHITESPACE_CHARS = '\n\r\t\b\\\u200b '


def is_integers(*args) -> bool:
    try:
        if len(args) > 0 and all([float(n).is_integer() for n in args]):
            return True

    except TypeError:
        return False
    except ValueError:
        return False

    return False


def is_numbers(*args) -> bool:
    try:
        if len(args) > 0 and all([isinstance(float(n), float) for n in args]):
            return True
    except TypeError:
        return False
    except ValueError:
        return False

    return False


def remove_spaces(text: str) -> str:
    """
    주어진 문자열에서 ('\\n', '\\r', '\\t', '\\b, '\\u200b', ' ' ) 문자들을 제거 합니다.


    :param text: 외부 문자열
    :type text: str
    :return: 변환된 문자열
    :rtype: Optional[str]

    :Example:
        >>> from gpp.texts import remove_spaces
        >>> remove_spaces('a')
        'a'
        >>> remove_spaces(' ')
        ''
        >>> remove_spaces(' a ')
        'a'
        >>> remove_spaces('\t\t\t\t\t\t\t\t\t\t\b a ')
        'a'
        >>> remove_spaces('\\n\\r\\t\\b \\u200b가\\n\\r\\t\\b \\u200b나\\n\\r\\t\\b \\u200b다\\n\\r\\t\\b \\u200b라\\n\\r\\t\\b \\u200b')
        '가나다라'
        >>> remove_spaces(-1)
        '-1'
        >>> remove_spaces(1)
        '1'
    """
    if not isinstance(text, str):
        text = str(text or '')

    for p in WHITESPACE_CHARS:
        text = text.replace(p, '')

    return text


def extract_hangul(text: str):
    """
    주어진 문자열에서 한글만 추출합니다.

    :param text: 외부 문자열
    :type text: str
    :return: 변환된 문자열
    :rtype: Optional[str]
    :Example:
        >>> from gpp.texts import extract_hangul
        >>> extract_hangul('가abc나')
        '가나'

    """
    if not isinstance(text, str):
        text = str(text)
    ret = HANGUL_PATTERN.findall(text)
    return ''.join(ret)


def convert_words(text: str):
    """
        단어들 사이에 있는 중복된 구분자들을 하나로 만듭니다.

    :param text: 외부 문자열
    :type text: str
    :param default: 오류 발생시 기본값
    :type default: Optional[str]
    :return: 변환된 문자열
    :rtype: Optional[str]
    :Example:
        >>> from gpp.texts import convert_words
        >>> convert_words('가   나')
        '가 나'
    """
    if not isinstance(text, str):
        text = str(text)

    return ' '.join(
        a for a in text.strip(WHITESPACE_CHARS).replace('\xa0', ' ').split() if a
    )


def convert_date(text: str, default: Optional[datetime.date] = None) -> datetime.date:
    """
        text에서 년월일을 추출 합니다.

    :param text: 외부 문자열
    :type text: str
    :param default: 오류 발생시 기본값
    :type default: Optional[datetime.date]
    :return: 년월일
    :rtype: Optional[datetime.date]
    :Example:
        >>> from gpp.texts import convert_date
        >>> convert_date('2023-01-01')
        datetime.date(2023, 1, 1)
        >>> convert_date('2023.01.01')
        datetime.date(2023, 1, 1)
        >>> convert_date('20230101')
        datetime.date(2023, 1, 1)
    """

    if not isinstance(text, str):
        text = str(text)

    text = TRIM_CHARS_PATTERN.sub('', text)
    text = remove_spaces(text)
    text = text.replace('.', '-').replace('\xa0', '')

    # format yyyymmdd
    if is_integers(text) and len(text) == 8:
        text = f'{text[:4]}-{text[4:6]}-{text[6:8]}'

    ret = text.split('-')
    if len(ret) == 3 and is_integers(*ret):
        year, month, day = tuple(map(int, ret))
        ret = dt(year=year, month=month, day=day)

        if ret:
            return ret.date()

    return default


def extract_integer_as_string(text: str, default: Optional[str] = None):
    """
    text에서 정수를 추출하여 문자열로 반환 합니다.

    :param text: 외부 문자열
    :type text: str
    :param default: 오류 발생시 기본값
    :type default: Optional[str]
    :return: 정수로 구성된 문자열
    :rtype: Optional[str]
    :Example:
        >>> from gpp.texts import extract_integer_as_string
        >>> extract_integer_as_string('584-87-01610')
        '5848701610'
        >>> extract_integer_as_string('서울02')
        '02'
    """
    if not isinstance(text, str):
        text = str(text)

    flag = ''
    text = NUMBER_PATTERN.sub('', text)
    text = remove_spaces(text)

    if text and text.startswith('-'):
        flag = '-'
    text = text.replace('.', '').replace('-', '').replace(',', '')

    if text:
        return f'{flag}{text}'

    return default


def extract_integer(text: str, default: Optional[int] = None):
    """
    text에서 정수를 추출하여 반환 합니다.

    :param text: 외부 문자열
    :type text: str
    :param default: 오류 발생시 기본값
    :type default: Optional[int]
    :return: 정수
    :rtype: Optional[int]
    :Example:
        >>> from gpp.texts import extract_integer
        >>> extract_integer('584-87-01610')
        5848701610
        >>> extract_integer('서울02')
        2
    """
    ret = extract_integer_as_string(text, default)
    if is_integers(ret):
        return int(ret)

    return default


def convert_integer(text: str, default: Optional[int] = None):
    """
    text에서 정수를 추출하여 반환 합니다.

    :param text: 외부 문자열
    :type text: str
    :param default: 오류 발생시 기본값
    :type default: Optional[int]
    :return: 정수
    :rtype: Optional[int]
    :Example:
        >>> from gpp.texts import convert_integer
        >>> convert_integer('584')
        584
        >>> convert_integer('서울02', 11)
        11
        >>> convert_integer('         02')
        2
    """
    number = convert_decimal(text, default)
    if isinstance(number, Decimal):
        return int(number)

    return default


def convert_decimal(text: str, default: Optional[Decimal] = None):
    """
    text에서 실수(소수점을 포함)를 추출하여 반환 합니다.

    :param text: 외부 문자열
    :type text: str
    :param default: 오류 발생시 기본값
    :type default: Optional[Decimal]
    :return: decimal
    :rtype: Optional[Decimal]
    :Example:
        >>> from gpp.texts import convert_decimal
        >>> convert_decimal('584.8701610')
        Decimal('584.8701610')
        >>> convert_decimal('-123.456789')
        Decimal('-123.456789')
    """
    text = remove_spaces(text)

    if is_numbers(text):
        num = Decimal(str(text))
        if num.is_finite():
            return num

    return default


def convert_money(text: str, unit: int = 1, default: Optional[int] = None) -> int:
    """
    text에서 정수를 추출하여 반환 합니다.

    :param text: 외부 문자열
    :type text: str
    :param unit: 단위
    :type unit: int
    :param default: 오류 발생시 기본값
    :type default: Optional[int]
    :return: 정수
    :rtype: Optional[int]
    :Example:
        >>> from gpp.texts import convert_money
        >>> convert_money('10,000', 1000, None)  # 단위 천원
        10000000
    """
    try:
        val = remove_spaces(text).split('.')

        if len(val) <= 2:
            val[0] = val[0].replace(',', '')
            return int(val[0]) * unit

    except Exception:
        pass

    return default


def convert_readable_filesize(num: Union[int, float], suffix="B") -> str:
    """
    파일크기 num을 사람이 읽을 수 있는 문자열로 변환하여 반환 합니다.

    :param num: 파일크기
    :type num: Union[int, float
    :param suffix: 문자열 끝에 붙일 첨자
    :return: 사람이 읽을 수 있는 문자열
    :rtype: str
    :Note:
        10^3이 아닌, 2^10으로 나눕니다.
    :Example:
        >>> from gpp.texts import convert_readable_filesize
        >>> convert_readable_filesize(10000, 'B')
        '9.8KiB'
        >>> convert_readable_filesize(1234567890.99, 'B')
        '1.1GiB'
        >>> convert_readable_filesize(12345678901234.99, 'B')
        '11.2TiB'
        >>> convert_readable_filesize(123456789012345678.99, 'B')
        '109.7PiB'
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def convert_readable_count(num: Union[int, float]) -> str:
    """
    수량 num을 사람이 읽을 수 있는 문자열로 변환하여 반환 합니다.

    :param num: 수량
    :type num: Union[int, float
    :rtype: str
    :Note:
        2^10이 아닌, 10^3으로 나눕니다.
    :Example:
        >>> from gpp.texts import convert_readable_count
        >>> convert_readable_count(10000)
        '10.0K'
        >>> convert_readable_count(1234567890.99)
        '1.2G'
        >>> convert_readable_count(1234567890123)
        '1.2T'
        >>> convert_readable_count(12345678901234.99)
        '12.3T'
        >>> convert_readable_count(123456789012345678.99)
        '123.5P'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1000:
            return f"{num:3.1f}{unit}"
        num /= 1000

    return f"{num:3.1f}Y"


def convert_readable_timedelta(seconds: int) -> str:
    """
    seconds(시간의 초)를 사람이 읽을 수 있는 문자열로 변환하여 반환 합니다.

    :param seconds: 수량
    :type seconds: int
    :rtype: str
    :Note:
        소수점은 버림 합니다.
    :Example:
        >>> from gpp.texts import convert_readable_timedelta
        >>> convert_readable_timedelta(-1)
        '1초 전'
        >>> convert_readable_timedelta(0)
        '지금'
        >>> convert_readable_timedelta(1)
        '1초 후'
        >>> convert_readable_timedelta(10000)
        '2시간 후'
        >>> convert_readable_timedelta(10000000)
        '3개월 후'
        >>> convert_readable_timedelta(86400)
        '1일 후'
        >>> convert_readable_timedelta(86399)
        '23시간 후'
        >>> convert_readable_timedelta(1234567890)
        '39년 후'
    """
    if seconds == 0:
        return '지금'
    elif seconds < 0:
        future = '전'
        seconds = -seconds
    else:
        future = '후'

    unit = [1, 60, 60, 24, 30, 12]
    suffix = ['초', '분', '시간', '일', '개월', '년']

    ret = ''
    for u, s in zip(unit, suffix):
        if seconds >= u:
            seconds /= u
            ret = '{0}{1} {2}'.format(int(seconds), s, future)
        else:
            break

    return ret
