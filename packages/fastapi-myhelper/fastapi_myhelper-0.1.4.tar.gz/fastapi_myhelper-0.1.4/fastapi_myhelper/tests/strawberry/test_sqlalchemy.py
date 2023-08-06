import pytest
from sqlalchemy import MetaData, Table, Column, String, Integer
from sqlalchemy.sql.expression import UnaryExpression
from sqlalchemy.orm.attributes import InstrumentedAttribute

from fastapi_myhelper.strawberry.sqlalchemy import create_order_by_enum


def test_order_by_create():
    table = Table(
        "user",
        MetaData(),
        Column("user_id", Integer, primary_key=True),
        Column("user_name", String(16), nullable=False),
        Column("email_address", String(60)),
        Column("nickname", String(50), nullable=False),
    )
    enum = create_order_by_enum(
        name='UserOrderBy',
        table=table,
        fields=['user_id', 'user_name']
    )
    assert hasattr(enum, 'user_id') and isinstance(enum.user_id.value, Column)
    assert hasattr(enum, 'user_name') and isinstance(enum.user_name.value, Column)
    assert hasattr(enum, 'desc_user_id') and isinstance(enum.desc_user_id.value, UnaryExpression)
    assert hasattr(enum, 'desc_user_name') and isinstance(enum.desc_user_name.value, UnaryExpression)
    assert not hasattr(enum, 'email_address')
    assert not hasattr(enum, 'nickname')
    assert not hasattr(enum, 'desc_email_address')
    assert not hasattr(enum, 'desc_nickname')
