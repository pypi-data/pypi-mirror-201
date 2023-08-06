import datetime as dt
import operator as op

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

from .utils import assert_string_minified


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


# region - date
def test_date_eq():
    query_params = DateTimeFilter(op.eq, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_date).compile()

    assert query.params == {'a_date_1': dt.date(2020, 6, 1)}
    assert 'datetable.a_date = :a_date_1' == query.string


def test_date_ne():
    query_params = DateTimeFilter(op.ne, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_date).compile()

    assert query.params == {'a_date_1': dt.date(2020, 6, 1)}
    assert 'datetable.a_date != :a_date_1' == query.string


def test_date_le():
    query_params = DateTimeFilter(op.le, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_date).compile()

    assert query.params == {'a_date_1': dt.date(2020, 6, 1)}
    assert 'datetable.a_date <= :a_date_1' == query.string


def test_date_lt():
    query_params = DateTimeFilter(op.lt, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_date).compile()

    assert query.params == {'a_date_1': dt.date(2020, 6, 1)}
    assert 'datetable.a_date < :a_date_1' == query.string


def test_date_ge():
    query_params = DateTimeFilter(op.ge, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_date).compile()

    assert query.params == {'a_date_1': dt.date(2020, 6, 1)}
    assert 'datetable.a_date >= :a_date_1' == query.string


def test_date_gt():
    query_params = DateTimeFilter(op.gt, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_date).compile()

    assert query.params == {'a_date_1': dt.date(2020, 6, 1)}
    assert 'datetable.a_date > :a_date_1' == query.string
# endregion


# region - datetime
def test_datetime_eq():
    query_params = DateTimeFilter(op.eq, dt.datetime(2020, 6, 1, 2, 20, 34))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 1, 2, 20, 34)}
    assert 'datetable.a_datetime = :a_datetime_1' == query.string


def test_datetime_ne():
    query_params = DateTimeFilter(op.ne, dt.datetime(2020, 6, 1, 2, 20, 34))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 1, 2, 20, 34)}
    assert 'datetable.a_datetime != :a_datetime_1' == query.string


def test_datetime_le():
    query_params = DateTimeFilter(op.le, dt.datetime(2020, 6, 1, 2, 20, 34))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 1, 2, 20, 34)}
    assert 'datetable.a_datetime <= :a_datetime_1' == query.string


def test_datetime_lt():
    query_params = DateTimeFilter(op.lt, dt.datetime(2020, 6, 1, 2, 20, 34))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 1, 2, 20, 34)}
    assert 'datetable.a_datetime < :a_datetime_1' == query.string


def test_datetime_ge():
    query_params = DateTimeFilter(op.ge, dt.datetime(2020, 6, 1, 2, 20, 34))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 1, 2, 20, 34)}
    assert 'datetable.a_datetime >= :a_datetime_1' == query.string


def test_datetime_gt():
    query_params = DateTimeFilter(op.gt, dt.datetime(2020, 6, 1, 2, 20, 34))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 1, 2, 20, 34)}
    assert 'datetable.a_datetime > :a_datetime_1' == query.string
# endregion


# region - date input, datetime column
def test_date_to_datetime_eq():
    query_params = DateTimeFilter(op.eq, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {
        'a_datetime_1': dt.datetime(2020, 6, 1),
        'a_datetime_2': dt.datetime(2020, 6, 2),
    }
    assert 'datetable.a_datetime >= :a_datetime_1 AND datetable.a_datetime < :a_datetime_2' == query.string


def test_date_to_datetime_ne():
    query_params = DateTimeFilter(op.ne, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {
        'a_datetime_1': dt.datetime(2020, 6, 1, 0, 0, 0),
        'a_datetime_2': dt.datetime(2020, 6, 2, 0, 0, 0),
    }
    assert 'datetable.a_datetime < :a_datetime_1 AND datetable.a_datetime >= :a_datetime_2' == query.string


def test_date_to_datetime_le():
    query_params = DateTimeFilter(op.le, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 1, 0, 0, 0)}
    assert 'datetable.a_datetime <= :a_datetime_1' == query.string


def test_date_to_datetime_lt():
    query_params = DateTimeFilter(op.lt, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 1, 0, 0, 0)}
    assert 'datetable.a_datetime < :a_datetime_1' == query.string


def test_date_to_datetime_ge():
    query_params = DateTimeFilter(op.ge, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 1, 0, 0, 0)}
    assert 'datetable.a_datetime >= :a_datetime_1' == query.string


def test_date_to_datetime_gt():
    query_params = DateTimeFilter(op.gt, dt.date(2020, 6, 1))
    query = query_params.get_filter(DateTable.a_datetime).compile()

    assert query.params == {'a_datetime_1': dt.datetime(2020, 6, 2, 0, 0, 0)}
    assert 'datetable.a_datetime >= :a_datetime_1' == query.string
# endregion


def test_multiple_date_gt_lt_ne():
    query_params = DateTimeFilterList(
        filters=[
            DateTimeFilter(op.gt, dt.date(2020, 6, 1)),
            DateTimeFilter(op.lt, dt.date(2020, 6, 30)),
            DateTimeFilter(op.ne, dt.date(2020, 6, 15)),
        ],
    )
    query = query_params.get_filters(DateTable.a_date).compile()

    assert query.params == {
        'a_date_1': dt.date(2020, 6, 1),
        'a_date_2': dt.date(2020, 6, 30),
        'a_date_3': dt.date(2020, 6, 15),
    }
    assert_string_minified(
        query.string,
        '''
        datetable.a_date > :a_date_1
        AND datetable.a_date < :a_date_2
        AND datetable.a_date != :a_date_3
        ''',
    )


def test_multiple_date_to_datetime_gt_lt_ne():
    query_params = DateTimeFilterList(
        filters=[
            DateTimeFilter(op.gt, dt.date(2020, 6, 1)),
            DateTimeFilter(op.lt, dt.date(2020, 6, 30)),
            DateTimeFilter(op.ne, dt.date(2020, 6, 15)),
        ],
    )
    query = query_params.get_filters(DateTable.a_datetime).compile()

    assert query.params == {
        'a_datetime_1': dt.datetime(2020, 6, 2),
        'a_datetime_2': dt.datetime(2020, 6, 30),
        'a_datetime_3': dt.datetime(2020, 6, 15),
        'a_datetime_4': dt.datetime(2020, 6, 16),
    }
    assert_string_minified(
        query.string,
        '''
        datetable.a_datetime >= :a_datetime_1
        AND datetable.a_datetime < :a_datetime_2
        AND datetable.a_datetime < :a_datetime_3
        AND datetable.a_datetime >= :a_datetime_4
        ''',
    )
