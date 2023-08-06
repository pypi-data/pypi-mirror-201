import pytest
import strawberry
import dataclasses

from fastapi_myhelper.strawberry.schemas import TypeBase


def test_schema_type_creation():
    @strawberry.type
    class UserType(TypeBase):
        id: int
        username: str
        email: str | None = None

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
            and fields['email'].default is None
            and fields['email'].type == (str | None)
    )


def test_schema_type_optional():
    @strawberry.type
    class UserType(TypeBase):
        id: int
        username: str
        email: str | None = None

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


def test_schema_input_creation():
    @strawberry.input
    class UserType(TypeBase):
        id: int
        username: str
        email: str | None = None

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
            and fields['email'].default is None
            and fields['email'].type == (str | None)
    )


def test_schema_input_optional():
    @strawberry.input
    class UserType(TypeBase):
        id: int
        username: str
        email: str | None = None

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





