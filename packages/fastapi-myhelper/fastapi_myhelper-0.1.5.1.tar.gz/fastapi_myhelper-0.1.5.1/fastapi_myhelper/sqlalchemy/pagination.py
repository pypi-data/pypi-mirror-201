from typing import Any
from sqlalchemy import select
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import UnaryExpression
from sqlalchemy.sql.operators import desc_op
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .utils import attrs_name_equality


def cursor_qs_pagination(
        qs: Select,
        cursor_field: InstrumentedAttribute,
        order_by: UnaryExpression | InstrumentedAttribute | None = None,
        first: int | None = None,
        after: Any | None = None
) -> Select:
    qs = qs.limit(first).order_by(order_by or cursor_field)
    order_by, is_desc = (
        order_by.element,
        getattr(order_by, 'modifier', None) == desc_op
    ) if isinstance(order_by, UnaryExpression) else (order_by, False)
    if not after:
        return qs
    if order_by is None or attrs_name_equality(cursor_field, order_by):
        qs = qs.where(
            cursor_field < after
            if is_desc else
            cursor_field > after
        )
    else:
        sub_qs = select(order_by).where(cursor_field == after)
        qs = qs.where(
            (order_by < sub_qs) | (
                (order_by == sub_qs) & (cursor_field < after)
            ) if is_desc else
            (order_by > sub_qs) | (
                    (order_by == sub_qs) & (cursor_field > after)
            )
        )
    return qs