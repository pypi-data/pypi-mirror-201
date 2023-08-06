from datetime import date
from decimal import Decimal

import pytest
from gpp.texts import remove_spaces, extract_hangul, convert_words, convert_date, extract_integer_as_string, \
    extract_integer, convert_decimal, convert_money, convert_readable_timedelta, convert_readable_filesize, \
    convert_readable_count, convert_integer, is_integers, is_numbers


@pytest.mark.parametrize(
    'args, expected', [
        ([None], False),
        ([object], False),
        ([], False),
        ([()], False),
        ([1.1], False),
        ([1], True),
        ([-1], True),
        ([0], True),
        ([1, None], False),
        ([1, object], False),
        ([1, []], False),
        ([1, ()], False),
        ([1, 1], True),
        ([1, 1.1], False),
        (['1.1'], False),
        (['1'], True),
        (['-1'], True),
        (['0'], True),
        (['1', None], False),
        (['1', object], False),
        (['1', []], False),
        (['1', ()], False),
        (['1', '1'], True),
        (['1', '1.1'], False),
    ]
)
def test_is_integers(args, expected):
    assert is_integers(*args) == expected


@pytest.mark.parametrize(
    'args, expected', [
        ([None], False),
        ([object], False),
        ([], False),
        ([()], False),
        ([1.1], True),
        ([1], True),
        ([-1], True),
        ([0], True),
        ([1, None], False),
        ([1, object], False),
        ([1, []], False),
        ([1, ()], False),
        ([1, 1], True),
        ([1, 1.1], True),
        (['1.1'], True),
        (['1'], True),
        (['-1'], True),
        (['0'], True),
        (['1', None], False),
        (['1', object], False),
        (['1', []], False),
        (['1', ()], False),
        (['1', 1], True),
        (['1', '1.1'], True),
    ]
)
def test_is_numbers(args, expected):
    assert is_numbers(*args) == expected


@pytest.mark.parametrize(
    'in_data, expected', [
        (None, ''),
        ([], ''),
        ({}, ''),
        ('a', 'a'),
        (' ', ''),
        (' a ', 'a'),
        ('\t\t\t\t\t\t\t\t\t\t\b a ', 'a'),
        ('\n\r\t\b \u200b가\n\r\t\b \u200b나\n\r\t\b \u200b다\n\r\t\b \u200b라\n\r\t\b \u200b', '가나다라'),
        (-1, '-1'),
        (1, '1'),
    ]
)
def test_remove_spaces(in_data, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = remove_spaces(text=in_data)

    ##########################################################
    # assertion
    assert ret == expected


@pytest.mark.parametrize(
    'address, expected', [
        ('우 : 13911 경기도 안양시 만안구 예술공원로 164-1 (안양동)', '우경기도안양시만안구예술공원로안양동'),
        ('	우 : 33 rue du Puits Romain, Boite 6, L-8070 Bertrange, Luxembourg', '우'),
        ('가abc나', '가나'),
        (None, ''),
        (1, ''),
        (object, ''),
        ([], ''),
        ({}, ''),
    ]
)
def test_extract_hangul(address, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = extract_hangul(address)

    ##########################################################
    # assertion
    assert ret == expected


@pytest.mark.parametrize(
    'address, expected', [
        ('1      가나     다', '1 가나 다'),
        ('1 가나 다', '1 가나 다'),
        (123, '123'),
        (-123, '-123'),
    ]
)
def test_convert_words(address, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = convert_words(address)

    ##########################################################
    # assertion
    assert ret == expected


@pytest.mark.parametrize(
    'in_data, default, expected', [
        (None, None, None),
        (1, None, None),
        (object, None, None),
        ([], None, None),
        ({}, None, None),
        ('', None, None),
        (' - - ', None, None),
        ('1-1-1', None, date(1, 1, 1)),
        ('2000-01-01', None, date(2000, 1, 1)),
        ('2000-1-1', None, date(2000, 1, 1)),
        ('2000.01.01', None, date(2000, 1, 1)),
        ('20000101', None, date(2000, 1, 1)),
        ('20009999', None, None),
        ('2018\xa0 - \xa003\xa0 - \xa029', None, date(2018, 3, 29)),
    ]
)
def test_convert_date(in_data, default, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = convert_date(text=in_data, default=default)

    ##########################################################
    # assertion
    assert ret == expected


@pytest.mark.parametrize(
    'in_data, default, expected', [
        ('', None, None),
        (' - - ', None, None),
        ('1-1-1', None, '111'),
        ('2000-01-01', None, '20000101'),
        ('2000-1-1', None, '200011'),
        ('2000.01.01', None, '20000101'),
        ('20000101', None, '20000101'),
        ('20009999', None, '20009999'),
        ('02  -  930  -  6665', None, '029306665'),
        ('02  -  6918  -  6152', None, '0269186152'),
        ('2018\xa0 - \xa003\xa0 - \xa029', None, '20180329'),
        ('584-87-01610', None, '5848701610'),
        ('서울02', None, '02'),
        (-1.1, None, '-11'),  # NOT convert to integer. 'extract'
        (1.1, None, '11'),  # NOT convert to integer. 'extract'
    ]
)
def test_extract_integer_as_string(in_data, default, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = extract_integer_as_string(text=in_data, default=default)

    ##########################################################
    # assertion
    assert ret == expected


@pytest.mark.parametrize(
    'in_data, default, expected', [
        (None, None, None),
        ([], None, None),
        ({}, None, None),
        ('', None, None),
        (' - - ', None, None),
        ('1-1-1', None, 111),
        ('2000-01-01', None, 20000101),
        ('2000-1-1', None, 200011),
        ('2000.01.01', None, 20000101),
        ('20000101', None, 20000101),
        ('20009999', None, 20009999),
        ('02  -  930  -  6665', None, 29306665),
        ('02  -  6918  -  6152', None, 269186152),
        ('2018\xa0 - \xa003\xa0 - \xa029', None, 20180329),
        ('584-87-01610', None, 5848701610),
        ('서울02', None, 2),
        (-1.1, None, -11),  # NOT convert to integer. 'extract'
        (1.1, None, 11),  # NOT convert to integer. 'extract'
    ]
)
def test_extract_integer(in_data, default, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = extract_integer(text=in_data, default=default)

    ##########################################################
    # assertion
    assert ret == expected


@pytest.mark.parametrize(
    'in_data, default, expected', [
        (None, None, None),
        ([], None, None),
        ({}, None, None),
        ('', None, None),
        (' - - ', None, None),
        ('1-1-1', None, None),
        ('2000-01-01', None, None),
        ('2000-1-1', None, None),
        ('2000.01.01', None, None),
        ('20000101', None, Decimal('20000101')),
        ('20009999', None, Decimal('20009999')),
        ('02  -  930  -  6665', None, None),
        ('02  -  6918  -  6152', None, None),
        ('2018\xa0 - \xa003\xa0 - \xa029', None, None),
        ('584-87-01610', None, None),
        ('서울02', None, None),
        (-1.1, None, Decimal('-1.1')),
        (1.1, None, Decimal('1.1')),
    ]
)
def test_convert_decimal(in_data, default, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = convert_decimal(text=in_data, default=default)

    ##########################################################
    # assertion
    assert ret == expected


@pytest.mark.parametrize(
    'in_data, default, expected', [
        (None, None, None),
        ([], None, None),
        ({}, None, None),
        ('', None, None),
        (' - - ', None, None),
        ('1-1-1', None, None),
        ('2000-01-01', None, None),
        ('2000-1-1', None, None),
        ('2000.01.01', None, None),
        ('20000101', None, 20000101),
        ('20009999', None, 20009999),
        ('-20000101', None, -20000101),
        ('-20009999', None, -20009999),
        ('02  -  930  -  6665', None, None),
        ('02  -  6918  -  6152', None, None),
        ('2018\xa0 - \xa003\xa0 - \xa029', None, None),
        ('584-87-01610', None, None),
        ('서울02', None, None),
        (-1.1, None, -1),
        (1.1, None, 1),
    ]
)
def test_convert_integer(in_data, default, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = convert_integer(text=in_data, default=default)

    ##########################################################
    # assertion
    assert ret == expected


@pytest.mark.parametrize(
    'in_data, unit, default, expected', [
        ('', 10, None, None),
        (' - - ', 10, None, None),
        ('1-1-1', 10, None, None),
        ('2000-01-01', 10, None, None),
        ('2000-1-1', 10, None, None),
        ('2000.01.01', 10, None, None),
        ('02  -  930  -  6665', 10, None, None),
        ('02  -  6918  -  6152', 10, None, None),
        ('2000.010.020', 10, None, None),
        ('2000.010020', 10, None, 20000),
        ('2,000.010020', 10, None, 20000),
        ('2,000,010,020', 10, None, 20000100200),
        ('-2000.010020', 10, None, -20000),
        ('-2,000.010020', 10, None, -20000),
        ('-2,000,010,020', 10, None, -20000100200),
    ]
)
def test_convert_money(in_data, unit, default, expected):
    ret = convert_money(text=in_data, unit=unit, default=default)

    assert ret == expected


@pytest.mark.parametrize(
    'size, expected', [
        (0, '0.0B'),
        (10000, '9.8KiB'),
        (1234567890.99, '1.1GiB'),
        (12345678901234.99, '11.2TiB'),
        (123456789012345678.99, '109.7PiB'),
        (123456789012345678123456123123.99, '102121.1 YiB'),
        (-10000, '-9.8KiB'),
        (-1234567890.99, '-1.1GiB'),
        (-12345678901234.99, '-11.2TiB'),
        (-123456789012345678.99, '-109.7PiB'),
        (-123456789012345678123456123123.99, '-102121.1 YiB'),
    ]
)
def test_convert_readable_filesize(size, expected):
    assert convert_readable_filesize(size, 'B') == expected


@pytest.mark.parametrize(
    'size, expected', [
        (0, '0.0'),
        (10000, '10.0K'),
        (1234567890.99, '1.2G'),
        (12345678901234.99, '12.3T'),
        (123456789012345678.99, '123.5P'),
        (123456789012345678123456123123.99, '123456.8Y'),
        (-10000, '-10.0K'),
        (-1234567890.99, '-1.2G'),
        (-12345678901234.99, '-12.3T'),
        (-123456789012345678.99, '-123.5P'),
        (-123456789012345678123456123123.99, '-123456.8Y'),
    ]
)
def test_convert_readable_count(size, expected):
    assert convert_readable_count(size) == expected


@pytest.mark.parametrize(
    'seconds, expected', [
        (0, '지금'),
        (1, '1초 후'),
        (60, '1분 후'),
        (3600, '1시간 후'),
        (86400, '1일 후'),
        (2592000, '1개월 후'),
        (31104000, '1년 후'),
        (62208000, '2년 후'),
        (-1, '1초 전'),
        (-60, '1분 전'),
        (-3600, '1시간 전'),
        (-86400, '1일 전'),
        (-2592000, '1개월 전'),
        (-31104000, '1년 전'),
        (-62208000, '2년 전'),
    ]
)
def test_human_days(seconds, expected):
    assert convert_readable_timedelta(seconds) == expected
