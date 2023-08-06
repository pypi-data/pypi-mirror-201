import pytest

from gpp.datetimes import dt, dt_first, dt_last, dt_first_with_delta, is_last_date, dt_last_with_delta


@pytest.mark.parametrize('year, month, day, hour, minute, second, microsecond', [
    (2000, 1, 1, 0, 0, 0, 0),
    (2000, 1, 1, 23, 59, 59, 999999),
    (2000, 12, 31, 0, 0, 0, 0),
    (2000, 12, 31, 23, 59, 59, 999999),
    (2000, 2, 28, 0, 0, 0, 0),
    (2000, 2, 28, 23, 59, 59, 999999),
    (2000, 2, 29, 0, 0, 0, 0),
    (2000, 2, 29, 23, 59, 59, 999999),
])
def test_dt(year, month, day, hour, minute, second, microsecond):
    ret = dt(year, month, day, hour, minute, second, microsecond)
    assert ret.year == year
    assert ret.month == month
    assert ret.day == day
    assert ret.hour == hour
    assert ret.minute == minute
    assert ret.second == second
    assert ret.microsecond == microsecond


@pytest.mark.parametrize(
    'year, month', [
        (2000, m) for m in range(1, 12)
    ]
)
def test_dt_first_day(year, month):
    ret = dt_first(year, month)
    assert ret.year == year
    assert ret.month == month
    assert ret.day == 1
    assert ret.hour == 0
    assert ret.minute == 0
    assert ret.second == 0
    assert ret.microsecond == 0


@pytest.mark.parametrize(
    'year, month, expect_year, expect_month, expect_day', [
        (2000, 1, 2000, 1, 31),
        (2000, 2, 2000, 2, 29),
        (2000, 3, 2000, 3, 31),
        (2000, 4, 2000, 4, 30),
        (2000, 5, 2000, 5, 31),
        (2000, 6, 2000, 6, 30),
        (2000, 7, 2000, 7, 31),
        (2000, 8, 2000, 8, 31),
        (2000, 9, 2000, 9, 30),
        (2000, 10, 2000, 10, 31),
        (2000, 11, 2000, 11, 30),
        (2000, 12, 2000, 12, 31),
        (2001, 1, 2001, 1, 31),
        (2001, 2, 2001, 2, 28),
        (2001, 3, 2001, 3, 31),
        (2001, 4, 2001, 4, 30),
        (2001, 5, 2001, 5, 31),
        (2001, 6, 2001, 6, 30),
        (2001, 7, 2001, 7, 31),
        (2001, 8, 2001, 8, 31),
        (2001, 9, 2001, 9, 30),
        (2001, 10, 2001, 10, 31),
        (2001, 11, 2001, 11, 30),
        (2001, 12, 2001, 12, 31),
    ]
)
def test_dt_last_day(year, month, expect_year, expect_month, expect_day):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = dt_last(year, month)

    ##########################################################
    # assertion
    assert ret.year == expect_year
    assert ret.month == expect_month
    assert ret.day == expect_day
    assert ret.hour == 23
    assert ret.minute == 59
    assert ret.second == 59
    assert ret.microsecond == 999999


@pytest.mark.parametrize(
    'year, month, delta_month, expect_year, expect_month', [
        (2000, 1, -13, 1998, 12),
        (2000, 1, -12, 1999, 1),
        (2000, 1, -1, 1999, 12),
        (2000, 1, 0, 2000, 1),
        (2000, 1, 1, 2000, 2),
        (2000, 1, 12, 2001, 1),
        (2000, 1, 13, 2001, 2),
    ]
)
def test_dt_first_with_delta(year, month, delta_month, expect_year, expect_month):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = dt_first_with_delta(year, month, delta_month)

    ##########################################################
    # assertion
    assert ret.year == expect_year
    assert ret.month == expect_month
    assert ret.day == 1
    assert ret.hour == 0
    assert ret.minute == 0
    assert ret.second == 0
    assert ret.microsecond == 0


@pytest.mark.parametrize(
    'year, month, delta_month, expect_year, expect_month, expected_day', [
        (2000, 1, -13, 1998, 12, 31),
        (2000, 1, -12, 1999, 1, 31),
        (2000, 1, -12.0, 1999, 1, 31),
        (2000, 1, -1, 1999, 12, 31),
        (2000, 1, 0, 2000, 1, 31),
        (2000, 1, 1, 2000, 2, 29),
        (2000, 1, 12, 2001, 1, 31),
        (2000, 1, 13, 2001, 2, 28),
    ]
)
def test_dt_last_with_delta(year, month, delta_month, expect_year, expect_month, expected_day):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret = dt_last_with_delta(year, month, delta_month)

    ##########################################################
    # assertion
    assert ret.year == expect_year
    assert ret.month == expect_month
    assert ret.day == expected_day
    assert ret.hour == 23
    assert ret.minute == 59
    assert ret.second == 59
    assert ret.microsecond == 999999


@pytest.mark.parametrize(
    'year, month, day, expected',
    [(2000, 2, day, False) for day in range(1, 28 + 1)] +
    [(2000, 2, 29, True)] +
    [(2000, 3, day, False) for day in range(1, 30 + 1)] +
    [(2000, 3, 31, True)]
)
def test_is_last_date(year, month, day, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function
    ret_dt = dt(year=year, month=month, day=day)
    ret = is_last_date(ret_dt)

    ##########################################################
    # assertion
    assert ret == expected
