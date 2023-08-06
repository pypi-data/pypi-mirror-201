from typing import Tuple
from gpp.constants import KST
from datetime import timedelta, datetime


def dt(year: int, month: int, day: int, h: int = 0, m: int = 0, s: int = 0, ms: int = 0) -> datetime:
    """
        년월일 객체를 만듭니다.

    :param year: 년
    :type year: int
    :param month: 월
    :type month: int
    :param day: 일
    :type day: int
    :param h: 시 (default=0)
    :type h: int
    :param m: 분 (default=0)
    :type m: int
    :param s: 초 (default=0)
    :type s: int
    :param ms: 마이크로초(0.000001) (default=0)
    :type ms: int
    :return: datetime 객체
    :rtype: datetime
    :Example:
        >>> from gpp.datetimes import dt
        >>> ret = dt(2023, 1, 1)
        >>> ret.year, ret.month, ret.day, ret.hour, ret.minute, ret.second, ret.microsecond
        (2023, 1, 1, 0, 0, 0, 0)
    """
    try:
        dt = datetime(year=year, month=month, day=day, hour=h, minute=m, second=s, microsecond=ms, tzinfo=KST)
        return dt
    except ValueError:
        return None


def dt_first(year: int, month: int) -> datetime:
    """
        주어진 년월의 가장 빠른 datetime을 반환 합니다.

    :param year: 년
    :type year: int
    :param month: 월
    :type month: int
    :return: datetime 객체
    :rtype: datetime
    """
    return dt(year=year, month=month, day=1)


def dt_last(year: int, month: int) -> datetime:
    """
        주어진 년월의 가장 늦은 datetime을 반환 합니다.

    :param year: 년
    :type year: int
    :param month: 월
    :type month: int
    :return: datetime 객체
    :rtype: datetime
    """
    if month == 12:
        first_datetime_of_next_month = dt_first(year + 1, 1)
    else:
        first_datetime_of_next_month = dt_first(year, month + 1)

    return first_datetime_of_next_month + timedelta(microseconds=-1)


def get_yearmonth_with_delta(year: int, month: int, delta_month: int) -> Tuple[int, int]:
    """
        주어진 년, 월에서 `delta_month` 개월 만큼 더한 년월을 반환합니다.

    :param year: 년
    :type year: int
    :param month: 월
    :type month: int
    :param delta_month: delta_month 개월
    :type delta_month: int
    :return: (년, 월)
    :rtype: Tuple[int, int]
    """
    if not isinstance(delta_month, int):
        delta_month = int(delta_month)

    if delta_month != 0:
        m = month + delta_month - 1
        delta_year = m // 12
        year += delta_year
        m -= delta_year * 12

        month = m + 1

    return year, month


def dt_first_with_delta(year: int, month: int, delta_month: int) -> datetime:
    """
        주어진 년, 월에서 `delta_month` 개월 만큼 더한 후 가장 빠른 datetime을 반환 합니다.

    :param year: 년
    :type year: int
    :param month: 월
    :type month: int
    :param delta_month: delta_month 개월
    :type delta_month: int
    :return: datetime 객체
    :rtype: datetime
    """
    year, month = get_yearmonth_with_delta(year=year, month=month, delta_month=delta_month)
    return dt_first(year=year, month=month)


def dt_last_with_delta(year: int, month: int, delta_month: int) -> datetime:
    """
        주어진 년, 월에서 `delta_month` 개월 만큼 더한 후 가장 늦은 datetime을 반환 합니다.

    :param year: 년
    :type year: int
    :param month: 월
    :type month: int
    :param delta_month: delta_month 개월
    :type delta_month: int
    :return: datetime 객체
    :rtype: datetime
    """
    year, month = get_yearmonth_with_delta(year=year, month=month, delta_month=delta_month)
    return dt_last(year=year, month=month)


def is_last_date(date: datetime.date) -> bool:
    """
        주어진 date가 해당월의 마지막 날짜인지 확인합니다.

    :param date: date
    :type date: datetime.date
    :return: 마지막날 맞는지 여부
    :rtype: bool
    """

    if isinstance(date, datetime):
        date = date.date()

    return dt_last(date.year, date.month).date() == date
