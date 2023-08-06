import strawberry

from typing import Any, Type, ForwardRef
from enum import Enum


def create_order_by_enum(
        name: str,
        fields: dict[str, Any],
) -> Type[Enum]:
    fields = {
        field: strawberry.enum_value(fields[field])
        for field in fields
    }
    return strawberry.enum(Enum(name, fields))
