import datetime as dt
import functools
import operator as op
import typing
from dataclasses import dataclass

import marshmallow.fields as mf
from marshmallow.utils import from_iso_date, from_iso_datetime, from_rfc
from marshmallow_dataclass import NewType
from sqlalchemy import Column, ColumnElement
from sqlalchemy.types import DateTime

operator_map = {
    '=': op.eq,
    '==': op.eq,
    '!=': op.ne,
    '>=': op.ge,
    '<=': op.le,
    '>': op.gt,
    '<': op.lt,
}


@dataclass
class DateTimeFilter:
    operator: typing.Callable[[typing.Any, typing.Any], typing.Any]
    value: typing.Union[dt.date, dt.datetime]

    def get_filter(self, column: Column) -> ColumnElement[bool]:
        '''
            Get SQLAlchemy filter.

            SQL doesn't handle date comparisons with dates as expected, so we'd have to add it ourselves
            This allows us to accept user input in a more natural way
            i.e.:
               '=2020-06-01' -> '>=2020-06-01T00:00:00,<2020-06-02T00:00:00'
               '!=2020-06-01' -> '<2020-06-01T00:00:00,>=2020-06-02T00:00:00'
               '>2020-06-01' -> '>=2020-06-02T00:00:00'
               '>=2020-06-01' -> '>=2020-06-01T00:00:00'
               '<2020-06-01' -> '<2020-06-1T00:00:00'
               '<=2020-06-01' -> '<=2020-06-01T00:00:00'
        '''
        if isinstance(column.type, DateTime) and not isinstance(self.value, dt.datetime):
            lower_bound = dt.datetime(
                    year=self.value.year,
                    month=self.value.month,
                    day=self.value.day,
            )
            upper_bound = dt.datetime(
                year=self.value.year,
                month=self.value.month,
                day=self.value.day,
            ) + dt.timedelta(days=1)

            if self.operator == op.eq:
                # '=2020-06-01' -> '>=2020-06-01T00:00:00,<2020-06-02T00:00:00'
                return (column >= lower_bound) & (column < upper_bound)
            elif self.operator == op.ne:
                # '!=2020-06-01' -> '<2020-06-01T00:00:00,>=2020-06-02T00:00:00'
                return (column < lower_bound) & (column >= upper_bound)
            elif self.operator == op.gt:
                # '>2020-06-01' -> '>=2020-06-02T00:00:00'
                return (column >= upper_bound)
            elif self.operator == op.ge:
                # '>=2020-06-01' -> '>=2020-06-01T00:00:00'
                return (column >= lower_bound)
            elif self.operator == op.lt:
                # '<2020-06-01' -> '<2020-06-1T00:00:00'
                return (column < lower_bound)
            elif self.operator == op.le:
                # '<=2020-06-01' -> '<=2020-06-01T00:00:00'
                return (column <= lower_bound)

        return self.operator(column, self.value)


@dataclass
class DateTimeFilterList:
    filters: typing.List[DateTimeFilter]

    def get_filters(self, column: Column) -> ColumnElement[bool]:
        '''Get SQLAlchemy filter'''
        return functools.reduce(op.and_, (f.get_filter(column) for f in self.filters))


class DateTimeFilterExpression(mf.DateTime):
    '''
        Marshmallow field for dealing with DateTimeFilters.

        Example:
            ">=2020-01-01T00:00:00,<2020-02-01T00:00:00,!=2020-01-15T00:00:00"
    '''

    DESERIALIZATION_FUNCS = {
        "iso": [from_iso_datetime, from_iso_date],
        "iso8601": [from_iso_datetime, from_iso_date],
        "rfc": [from_rfc],
        "rfc822": [from_rfc],
    }  # type: typing.Dict[str, typing.List[typing.Callable[[str], typing.Any]]]

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None

        if isinstance(value, DateTimeFilter):
            return self._serialize_dtfilter(value)
        elif isinstance(value, DateTimeFilterList):
            return ','.join(self._serialize_dtfilter(f) for f in value.filters)
        elif isinstance(value, dict):
            return self._serialize_dtfilter_dict(value)
        elif isinstance(value, list):
            return ','.join(self._serialize_dtfilter_dict(f) for f in value)
        else:
            raise TypeError('DateTimeFilterExpression expects a DateTimeFilter, DateTimeFilterList, dict, or list')

    def _deserialize(self, value: str, attr, data, **kwargs):
        if not value:  # Falsy values, e.g. '', None, [] are not valid
            raise self.make_error("invalid", input=value, obj_type=self.OBJ_TYPE)

        filters = value.split(',')
        dt_filters = []
        for filter_ in filters:
            dt_operator = '='
            dt_value = filter_
            if ''.join(filter_[0:2]) in ('==', '!=', '>=', '<='):
                dt_operator = filter_[:2]
                dt_value = filter_[2:]
            elif filter_[0] in ('=', '>', '<'):
                dt_operator = filter_[0]
                dt_value = filter_[1:]

            # We should never get here. Since we allow no operator be defined, we just try to parse the date.
            if dt_operator not in operator_map:
                raise ValueError(f"Unknown operator. Must be one of {','.join(operator_map)}")

            dt_filter = DateTimeFilter(
                operator=operator_map[dt_operator],
                value=self._deserialize_dt_value(dt_value),
            )
            dt_filters.append(dt_filter)

        return DateTimeFilterList(filters=dt_filters)

    def _serialize_dtfilter(self, value: DateTimeFilter):
        return f'{value.operator}{self._serialize_dt_value(value.value)}'

    def _serialize_dtfilter_dict(self, value):
        if isinstance(value, dict) and 'value' in value:
            return f'{value.get("operator", "=")}{self._serialize_dt_value(value["value"])}'
        else:
            raise ValueError('DateTimeFilter dict requires a "value" key pair.')

    def _serialize_dt_value(self, value: dt.date | dt.datetime):
        data_format = self.format or self.DEFAULT_FORMAT
        format_func = self.SERIALIZATION_FUNCS.get(data_format)
        if format_func:
            return format_func(value)
        else:
            return value.strftime(data_format)

    def _deserialize_dt_value(self, value: dt.date | dt.datetime):
        data_format = self.format or self.DEFAULT_FORMAT
        funcs = self.DESERIALIZATION_FUNCS.get(data_format)
        if funcs:
            try:
                # Loop through all functions, and return the first that returns successfully
                # If they all fail, raise the latest error
                func_error = None
                for func in funcs:
                    func_error = None  # reset
                    try:
                        return func(value)
                    except (TypeError, AttributeError, ValueError) as error:
                        func_error = error

                if func_error:
                    raise func_error

            except (TypeError, AttributeError, ValueError) as error:
                raise self.make_error(
                    "invalid", input=value, obj_type=self.OBJ_TYPE,
                ) from error
        else:
            try:
                return self._make_object_from_format(value, data_format)
            except (TypeError, AttributeError, ValueError) as error:
                raise self.make_error(
                    "invalid", input=value, obj_type=self.OBJ_TYPE,
                ) from error


DateTimeFilterType = NewType("DateTimeFilterType", DateTimeFilterList, field=DateTimeFilterExpression)
