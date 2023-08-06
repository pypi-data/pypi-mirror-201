from typing import Any

import marshmallow as ma
import sqlalchemy as sa
from marshmallow_dataclass import dataclass as ma_dataclass
from sqlalchemy.orm import Query, class_mapper

from ..fields import optional_field


class SortException(Exception):
    pass


@ma_dataclass
class SortableQueryParameters:
    sort: str = optional_field(
        help='''
            Used to sort the results. Format: "{column}:{direction}". Direction is optional.
            To filter by multiple columns, separate by comma. Example: "sort=country,city:desc"
        ''',
    )

    @ma.validates_schema
    def sort_validator(self: ma.Schema, data: dict, **kwargs):
        sort_data: str = data.get('sort')
        if not sort_data or sort_data == 'None':
            return

        errors = []
        parts = sort_data.split(',')
        for part in parts:
            field_parts = part.split(':', 1)
            if not field_parts:
                errors.append('Sort must specify a column name')
                continue

            # Validate that the field name is defined and that sorting is enabled
            if field_parts[0] and (self.declared_fields.get(field_parts[0], {}).metadata.get('sortable', False)):
                errors.append(f"Invalid sort column '{field_parts[0]}'.")
            if len(field_parts) == 2 and field_parts[1].lower() not in ('asc', 'desc'):
                errors.append("Invalid sort direction. Must be 'asc', or 'desc'.")

        if errors:
            raise ma.ValidationError({'sort': errors})

    def apply_sort(self, query: Query, db_model: Any) -> Query:
        '''
            Parses `sort` string and adds order by clauses to the query.
            Default direction is ascending.
            Expected format:
            * comma delimited columns
            * columns and direction delimited by colon

            Example:
                `given_name:desc,family_name`
            This is equivelent to SQL:
                `ORDER BY "given_name" DESC, "family_name" ASC`
        '''
        query = query._clone()

        sort_columns = filter(None, self.sort.split(','))  # filter out empty strings
        for sort_column in sort_columns:
            parts = sort_column.split(':')
            # Ignore empty parts
            if not parts:
                continue
            # Validate that sorted column exists.
            elif parts[0] not in [x.key for x in class_mapper(db_model).iterate_properties]:
                raise SortException("Sort column '{}' is not supported.".format(parts[0]))

            if len(parts) == 1:
                query = query.order_by(sa.asc(getattr(db_model, parts[0])))
            else:
                direction = parts[1].upper()
                if direction == 'ASC':
                    query = query.order_by(sa.asc(getattr(db_model, parts[0])))
                elif direction == 'DESC':
                    query = query.order_by(sa.desc(getattr(db_model, parts[0])))
                else:
                    raise SortException("Invalid sort direction. '{}'".format(direction))

        return query
