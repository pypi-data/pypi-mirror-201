import pytest
import strawberry

from fastapi_myhelper.strawberry.schemas import TypeBase
from fastapi_myhelper.strawberry.decorators import validator
from fastapi_myhelper.strawberry.exceptions import ValidationError, MultipleValidationErrors


def test_select_field_validator():
    @strawberry.input
    class UserType(TypeBase):
        id: int
        username: int
        email: int | None = None

        @validator('username')
        def username_min_length(cls, username: str):
            if len(username) < 3:
                raise ValidationError('Min length is 3')

    error = None
    try:
        user = UserType(id=1, username='iurg')
    except MultipleValidationErrors as e:
        error = e

    assert error is None

    try:
        user = UserType(id=1, username='iu')
    except MultipleValidationErrors as e:
        error = e

    assert error is not None
    assert isinstance(error, MultipleValidationErrors)
    assert len(error) == 1
    assert isinstance(error[0], ValidationError)


def test_all_fields_validator():
    @strawberry.input
    class UserType(TypeBase):
        id: int
        username: int
        email: int | None = None

        @validator(all_fields=True)
        def username_min_length(
                cls,
                username: str,
                id: int,
                email: str):
            if len(username) < 3:
                raise ValidationError('Min length is 3')
            if id != 1:
                raise ValidationError('id must be equal 1')
            if email is not None:
                raise ValidationError('')

    error = None
    try:
        user = UserType(id=1, username='iurg')
    except MultipleValidationErrors as e:
        error = e

    assert error is None

    try:
        user = UserType(id=1, username='iu')
    except MultipleValidationErrors as e:
        error = e

    assert error is not None
    assert isinstance(error, MultipleValidationErrors)
    assert len(error) == 1
    assert isinstance(error[0], ValidationError)
