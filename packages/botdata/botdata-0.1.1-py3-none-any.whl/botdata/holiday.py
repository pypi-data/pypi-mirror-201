from datetime import date, datetime, timedelta
from functools import lru_cache
from typing import List, TypeVar

import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay

"""
Holiday
"""


def get_holidays(year: int) -> List[date]:
    """Get holidays from Bank of Thailand website https://www.bot.or.th/Thai/FinancialInstitutions/FIholiday

    Parameters
    ----------
    year : int
        Year

    Returns
    -------
    List[date]
        List of holidays
    """
    return get_holidays_series(year=year).map(lambda x: x.date()).tolist()


@lru_cache
def get_holidays_series(year: int) -> pd.Series:
    """Get holidays from Bank of Thailand website https://www.bot.or.th/Thai/FinancialInstitutions/FIholiday

    Parameters
    ----------
    year : int
        Year

    Returns
    -------
    pd.Series
        Series of holidays
    """
    # df should contains the following columns: Index, Day of week, Day of month, Month, Description
    df = pd.read_html(
        f"https://www.bot.or.th/English/FinancialInstitutions/FIholiday/Pages/{year}.aspx"
    )[0]

    # Drop incorrect row usually from recursive
    df = df.dropna(axis=0, how="any", subset=[2, 3])
    # Drop cancelled holiday
    df = df[~df[4].str.contains("cancelled", case=False, na=False)]
    # Concat Day, Month, Year
    date_str_ser = df[2].astype(str).str[:-2] + " " + df[3] + " " + str(year)
    # Remove non-ascii characters usually unicode
    date_str_ser = date_str_ser.str.encode("ascii", "ignore").str.decode("ascii")

    return pd.to_datetime(date_str_ser)


def is_holiday(date_: date) -> bool:
    """Check if date is holiday

    Parameters
    ----------
    date_ : date
        Date

    Returns
    -------
    bool
        True if date is holiday
    """
    return date_ in get_holidays(date_.year)


"""
Business Day
"""


def is_business_day(date_: date) -> bool:
    """Check if date is business day

    Parameters
    ----------
    date_ : date
        Date

    Returns
    -------
    bool
        True if date is business day
    """
    return date_.weekday() < 5 and not is_holiday(date_)


T = TypeVar("T", bound=date)


def next_business_day(date_: T, n: int = 1) -> T:
    """Next business day

    Parameters
    ----------
    date_ : date
        Date
    n : int, optional
        n business days, can be negative, by default 1

    Returns
    -------
    date
        Date of next business day
    """
    holidays = get_holidays_series(date_.year).tolist()

    next_date = date_ + timedelta(n + 5 if n > 0 else n - 5)

    if next_date.year != date_.year:
        holidays += get_holidays_series(next_date.year).tolist()

    bd = CustomBusinessDay(n, holidays=holidays)

    ts = date_ + bd
    if type(date_) is date:
        return ts.date()  # type: ignore
    elif type(date_) is datetime:
        return ts.to_pydatetime()  # type: ignore
    else:
        return ts
