import pytest
from sqlmodel import SQLModel, Field
from sqlalchemy.sql.expression import UnaryExpression
from sqlalchemy.orm.attributes import InstrumentedAttribute

from fastapi_myhelper.strawberry.sqlmodel import create_order_by_enum


def test_create_order_by():
    class UserModel(SQLModel, table=True):
        id: int = Field(primary_key=True, nullable=True)
        username: str
        email: str

    enum = create_order_by_enum(
        name='UserOrderBy',
        model=UserModel,
        fields=['id', 'username']
    )

    assert hasattr(enum, 'id') and isinstance(enum.id.value, InstrumentedAttribute)
    assert hasattr(enum, 'username') and isinstance(enum.username.value, InstrumentedAttribute)
    assert hasattr(enum, 'desc_id') and isinstance(enum.desc_id.value, UnaryExpression)
    assert hasattr(enum, 'desc_username') and isinstance(enum.desc_username.value, UnaryExpression)
    assert not hasattr(enum, 'email')
    assert not hasattr(enum, 'desc_email')
