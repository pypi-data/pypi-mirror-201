import pytest
import strawberry
from strawberry.type import StrawberryOptional
import dataclasses

from fastapi_myhelper.strawberry.schemas import TypeBase
from fastapi_myhelper.strawberry.exceptions import ValidationError
from pydantic import BaseModel


def test_pydantic_type_creation():
    class UserModel(BaseModel):
        id: int
        username: str
        email: str | None = None

    @strawberry.experimental.pydantic.type(model=UserModel)
    class UserType(TypeBase, pydantic_schema=True):
        id: strawberry.auto
        username: strawberry.auto
        email: strawberry.auto

    assert isinstance(UserType, type)
    assert hasattr(UserType, '__dataclass_fields__')
    fields = UserType.__dataclass_fields__

    assert (
            'id' in fields
            and fields['id'].default is dataclasses.MISSING
            and fields['id'].type == int
    )
    assert (
            'username' in fields
            and fields['username'].default is dataclasses.MISSING
            and fields['username'].type == str
    )
    assert (
            'email' in fields
            and (
                    fields['email'].default is None
                    or hasattr(fields['email'].default_factory, '__call__')
            )
            and (
                    fields['email'].type == (str | None)
                    or isinstance(fields['email'].type, StrawberryOptional)
            )
    )


def test_pydantic_type_optional():
    class UserModel(BaseModel):
        id: int
        username: str
        email: str | None = None

    @strawberry.experimental.pydantic.type(model=UserModel)
    class UserType(TypeBase, pydantic_schema=True):
        id: strawberry.auto
        username: strawberry.auto
        email: strawberry.auto

        class Config:
            optional = {
                'fields': ['username', 'email'],
            }

    assert isinstance(UserType, type)
    assert hasattr(UserType, '__dataclass_fields__')
    fields = UserType.__dataclass_fields__
    assert (
            'id' in fields
            and fields['id'].default is dataclasses.MISSING
            and fields['id'].type == int
    )
    assert (
            'username' in fields
            and fields['username'].default is strawberry.UNSET
            and fields['username'].type == str | None
    )
    assert (
            'email' in fields
            and fields['email'].default is strawberry.UNSET
            and fields['email'].type == (str | None)
    )


def test_pydantic_input_creation():
    class UserModel(BaseModel):
        id: int
        username: str
        email: str | None = None

    @strawberry.experimental.pydantic.input(model=UserModel)
    class UserType(TypeBase, pydantic_schema=True):
        id: strawberry.auto
        username: strawberry.auto
        email: strawberry.auto

    assert isinstance(UserType, type)
    assert hasattr(UserType, '__dataclass_fields__')
    fields = UserType.__dataclass_fields__

    assert (
            'id' in fields
            and fields['id'].default is dataclasses.MISSING
            and fields['id'].type == int
    )
    assert (
            'username' in fields
            and fields['username'].default is dataclasses.MISSING
            and fields['username'].type == str
    )
    assert (
            'email' in fields
            and (
                    fields['email'].default is None
                    or hasattr(fields['email'].default_factory, '__call__')
            )
            and (
                    fields['email'].type == (str | None)
                    or isinstance(fields['email'].type, StrawberryOptional)
            )
    )


def test_pydantic_input_optional():
    class UserModel(BaseModel):
        id: int
        username: str
        email: str | None = None

    @strawberry.experimental.pydantic.input(model=UserModel)
    class UserType(TypeBase, pydantic_schema=True):
        id: strawberry.auto
        username: strawberry.auto
        email: strawberry.auto

        class Config:
            optional = {
                'fields': ['username', 'email'],
            }

    assert isinstance(UserType, type)
    assert hasattr(UserType, '__dataclass_fields__')
    fields = UserType.__dataclass_fields__
    assert (
            'id' in fields
            and fields['id'].default is dataclasses.MISSING
            and fields['id'].type == int
    )
    assert (
            'username' in fields
            and fields['username'].default is strawberry.UNSET
            and fields['username'].type == str | None
    )
    assert (
            'email' in fields
            and fields['email'].default is strawberry.UNSET
            and fields['email'].type == (str | None)
    )
