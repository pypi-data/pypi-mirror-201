from typing import Type
from enum import Enum
from sqlalchemy import Table, desc

from ..utils import create_order_by_enum as _create_order_by_enum


def create_order_by_enum(
        name: str,
        table: Type[Table] | Table,
        fields: list[str],
) -> Type[Enum]:
    new_fields = {}
    for field in fields:
        value = getattr(table.columns, field)
        new_fields[field] = value
        new_fields[f'desc_{field}'] = desc(value)
    return _create_order_by_enum(
        name=name,
        fields=new_fields
    )

