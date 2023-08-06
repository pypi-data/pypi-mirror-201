from datetime import date, datetime
from unittest.mock import ANY

import pandas as pd
import pytest

import botdata as bd


@pytest.mark.parametrize(
    ("year", "expected"),
    [
        (
            2020,
            [
                date(2020, 1, 1),
                date(2020, 2, 10),
                date(2020, 4, 6),
                date(2020, 5, 1),
                date(2020, 5, 4),
                date(2020, 5, 6),
                date(2020, 6, 3),
                date(2020, 7, 6),
                date(2020, 7, 27),
                date(2020, 7, 28),
                date(2020, 8, 12),
                date(2020, 9, 4),
                date(2020, 9, 7),
                date(2020, 10, 13),
                date(2020, 10, 23),
                date(2020, 12, 7),
                date(2020, 12, 10),
                date(2020, 12, 11),
                date(2020, 12, 31),
            ],
        ),
        (
            2022,
            [
                date(2022, 1, 3),
                date(2022, 2, 16),
                date(2022, 4, 6),
                date(2022, 4, 13),
                date(2022, 4, 14),
                date(2022, 4, 15),
                date(2022, 5, 2),
                date(2022, 5, 4),
                date(2022, 5, 16),
                date(2022, 6, 3),
                date(2022, 7, 13),
                date(2022, 7, 28),
                date(2022, 7, 29),
                date(2022, 8, 12),
                date(2022, 10, 13),
                date(2022, 10, 14),
                date(2022, 10, 24),
                date(2022, 12, 5),
                date(2022, 12, 12),
            ],
        ),
        (2000, [ANY] * 13),
        (2005, [ANY] * 15),
        (2010, [ANY] * 19),
        (2015, [ANY] * 18),
        (2021, [ANY] * 20),
        (2023, ANY),
    ],
)
def test_get_holidays(year: int, expected: list):
    # Test
    result = bd.get_holidays(year)

    # Check
    assert result == expected


@pytest.mark.parametrize(
    (("date_", "expected")),
    [
        (date(2020, 1, 1), True),
        (date(2020, 1, 2), False),
    ],
)
def test_is_holiday(date_: date, expected: bool):
    # Test
    result = bd.is_holiday(date_)

    # Check
    assert result is expected


@pytest.mark.parametrize(
    (("date_", "expected")),
    [
        (date(2020, 1, 1), False),
        (date(2020, 1, 2), True),
        (date(2020, 1, 3), True),
        (date(2020, 1, 4), False),
        (date(2020, 1, 5), False),
    ],
)
def test_is_business_day(date_: date, expected: bool):
    # Test
    result = bd.is_business_day(date_)

    # Check
    assert result is expected


@pytest.mark.parametrize(
    (("date_", "n", "expected")),
    [
        # test date
        (date(2020, 1, 1), 1, date(2020, 1, 2)),
        (date(2020, 1, 2), 1, date(2020, 1, 3)),
        (date(2020, 1, 3), 1, date(2020, 1, 6)),
        (date(2020, 1, 4), 1, date(2020, 1, 6)),
        (date(2020, 1, 5), 1, date(2020, 1, 6)),
        # test n
        (date(2020, 1, 1), 0, date(2020, 1, 2)),
        (date(2020, 1, 2), 0, date(2020, 1, 2)),
        (date(2020, 1, 1), -1, date(2019, 12, 30)),
        (date(2020, 1, 2), -1, date(2019, 12, 30)),
        (date(2020, 12, 30), 1, date(2021, 1, 4)),
        (date(2020, 12, 31), 1, date(2021, 1, 4)),
        # test datatype
        (datetime(2020, 1, 1), 1, datetime(2020, 1, 2)),
        (pd.Timestamp(2020, 1, 1), 1, pd.Timestamp(2020, 1, 2)),
    ],
)
def test_next_business_day(date_: date, n: int, expected: bool):
    # Test
    result = bd.next_business_day(date_=date_, n=n)

    # Check
    assert result == expected
    assert type(result) == type(date_)
