import datetime as dt
import operator as op

import marshmallow as ma
import pytest
import sqlalchemy.types as st
from marshmallow_dataclass import dataclass as ma_dataclass
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase

from marshmallow_api_utils.ma_dataclass import MaDataclass
from marshmallow_api_utils.models.date_time_filter import (
    DateTimeFilter,
    DateTimeFilterList,
    DateTimeFilterType,
)


class Base(DeclarativeBase):
    pass


class DateTable(Base):
    __tablename__ = 'datetable'

    id = Column(st.Integer, primary_key=True)

    a_date = Column(st.Date)
    a_datetime = Column(st.DateTime)


@ma_dataclass
class APIQueryParamsDTO(MaDataclass):
    a_date: DateTimeFilterType
    a_datetime: DateTimeFilterType


# region - test all operators
def test_parse_eq_expressions():
    query_params = APIQueryParamsDTO.loads('{"a_date": "=2020-06-01", "a_datetime": "==2020-06-01T02:20:34"}')

    assert query_params == APIQueryParamsDTO(
        a_date=DateTimeFilterList(
            filters=[DateTimeFilter(op.eq, dt.date(2020, 6, 1))],
        ),
        a_datetime=DateTimeFilterList(
            filters=[DateTimeFilter(op.eq, dt.datetime(2020, 6, 1, 2, 20, 34))],
        ),
    )


def test_parse_ne_expressions():
    query_params = APIQueryParamsDTO.loads(
        '{"a_date": "!=2020-06-01", "a_datetime": "!=2020-06-01T02:20:34"}',
    )

    assert query_params == APIQueryParamsDTO(
        a_date=DateTimeFilterList(
            filters=[DateTimeFilter(op.ne, dt.date(2020, 6, 1))],
        ),
        a_datetime=DateTimeFilterList(
            filters=[DateTimeFilter(op.ne, dt.datetime(2020, 6, 1, 2, 20, 34))],
        ),
    )


def test_parse_le_expressions():
    query_params = APIQueryParamsDTO.loads(
        '{"a_date": "<=2020-06-01", "a_datetime": "<=2020-06-01T02:20:34"}',
    )

    assert query_params == APIQueryParamsDTO(
        a_date=DateTimeFilterList(
            filters=[DateTimeFilter(op.le, dt.date(2020, 6, 1))],
        ),
        a_datetime=DateTimeFilterList(
            filters=[DateTimeFilter(op.le, dt.datetime(2020, 6, 1, 2, 20, 34))],
        ),
    )


def test_parse_lt_expressions():
    query_params = APIQueryParamsDTO.loads(
        '{"a_date": "<2020-06-01", "a_datetime": "<2020-06-01T02:20:34"}',
    )

    assert query_params == APIQueryParamsDTO(
        a_date=DateTimeFilterList(
            filters=[DateTimeFilter(op.lt, dt.date(2020, 6, 1))],
        ),
        a_datetime=DateTimeFilterList(
            filters=[DateTimeFilter(op.lt, dt.datetime(2020, 6, 1, 2, 20, 34))],
        ),
    )


def test_parse_ge_expressions():
    query_params = APIQueryParamsDTO.loads(
        '{"a_date": ">=2020-06-01", "a_datetime": ">=2020-06-01T02:20:34"}',
    )

    assert query_params == APIQueryParamsDTO(
        a_date=DateTimeFilterList(
            filters=[DateTimeFilter(op.ge, dt.date(2020, 6, 1))],
        ),
        a_datetime=DateTimeFilterList(
            filters=[DateTimeFilter(op.ge, dt.datetime(2020, 6, 1, 2, 20, 34))],
        ),
    )


def test_parse_gt_expressions():
    query_params = APIQueryParamsDTO.loads(
        '{"a_date": ">2020-06-01", "a_datetime": ">2020-06-01T02:20:34"}',
    )

    assert query_params == APIQueryParamsDTO(
        a_date=DateTimeFilterList(
            filters=[DateTimeFilter(op.gt, dt.date(2020, 6, 1))],
        ),
        a_datetime=DateTimeFilterList(
            filters=[DateTimeFilter(op.gt, dt.datetime(2020, 6, 1, 2, 20, 34))],
        ),
    )


def test_parse_multiple_expressions():
    query_params = APIQueryParamsDTO.loads('''
        {"a_date": ">2020-06-01,<2020-06-30,!=2020-06-15",
        "a_datetime": ">=2020-06-01T01:10:14,<=2020-06-30T02:20:24,!=2020-06-15T03:30:34"}
    ''')

    assert query_params == APIQueryParamsDTO(
        a_date=DateTimeFilterList(
            filters=[
                DateTimeFilter(op.gt, dt.date(2020, 6, 1)),
                DateTimeFilter(op.lt, dt.date(2020, 6, 30)),
                DateTimeFilter(op.ne, dt.date(2020, 6, 15)),
            ],
        ),
        a_datetime=DateTimeFilterList(
            filters=[
                DateTimeFilter(op.ge, dt.datetime(2020, 6, 1, 1, 10, 14)),
                DateTimeFilter(op.le, dt.datetime(2020, 6, 30, 2, 20, 24)),
                DateTimeFilter(op.ne, dt.datetime(2020, 6, 15, 3, 30, 34)),
            ],
        ),
    )
# endregion


# region
def test_parse_missing_operator():
    query_params = APIQueryParamsDTO.loads('{"a_date": "2020-06-01", "a_datetime": "2020-06-01T02:20:34"}')

    assert query_params == APIQueryParamsDTO(
        a_date=DateTimeFilterList(
            filters=[DateTimeFilter(op.eq, dt.date(2020, 6, 1))],
        ),
        a_datetime=DateTimeFilterList(
            filters=[DateTimeFilter(op.eq, dt.datetime(2020, 6, 1, 2, 20, 34))],
        ),
    )


def test_parse_invalid_operator():
    with pytest.raises(ma.ValidationError) as ex:
        APIQueryParamsDTO.loads('{"a_date": "=>2020-06-01", "a_datetime": ">>2020-06-01T02:20:34"}')

        assert ex.value.data == {
            'a_datetime': ['Not a valid datetime.'],
            'a_date': ['Not a valid datetime.'],
        }


def test_parse_invalid_date_without_operator():
    with pytest.raises(ma.ValidationError) as ex:
        APIQueryParamsDTO.loads('{"a_date": "20adfss20-06-01", "a_datetime": "2020-06-35T02:20:34"}')

        assert ex.value.data == {
            'a_datetime': ['Not a valid datetime.'],
            'a_date': ['Not a valid datetime.'],
        }


def test_parse_invalid_date_with_operator():
    with pytest.raises(ma.ValidationError) as ex:
        APIQueryParamsDTO.loads('{"a_date": ">=20adfss20-06-01", "a_datetime": "<=2020-06-35T02:20:34"}')

        assert ex.value.data == {
            'a_datetime': ['Not a valid datetime.'],
            'a_date': ['Not a valid datetime.'],
        }
# endregion
