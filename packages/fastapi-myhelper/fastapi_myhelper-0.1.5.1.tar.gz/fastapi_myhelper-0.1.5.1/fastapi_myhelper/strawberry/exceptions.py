from abc import ABC
from typing import (
    Type,
    Self,
    Generic,
    TypeVar,
    Any,
    Iterable
)

T = TypeVar('T')


class BaseError(Exception, ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__


class MultipleExceptionsBase(Exception, ABC, Generic[T]):
    errors: list[T | Type[T]]

    def __init__(self, *errors: T | Type[T]):
        self.errors = list(errors)

    def __iter__(self) -> T | Type[T]:
        for error in self.errors:
            yield error

    def __getitem__(self, index: int) -> T | Type[T]:
        return self.errors[index]

    def __len__(self) -> int:
        return len(self.errors)

    def __bool__(self) -> bool:
        return bool(self.errors)

    def __copy__(self) -> list[T | Type[T]]:
        return self.errors.copy()

    def __contains__(self, item: T | Type[T]) -> bool:
        return item in self.errors

    def __add__(self, other: Self) -> Self:
        self.errors = self.errors + other.errors
        return self


class ValidationError(BaseError):
    name = 'ValidationError'

    def __init__(
            self,
            message: str,
            *,
            path: list[str] | None = None,
            value: Any = None
    ):
        self.message = message
        self.path = path or []
        self.value = value

    def __str__(self):
        return self.message


class MultipleValidationErrors(MultipleExceptionsBase[ValidationError]):
    def __init__(self, *errors: ValidationError, schema_name: str):
        self.errors = list(errors)
        self.schema_name: str = schema_name

    def __str__(self) -> str:
        errors = '\n'.join([f"-\t{error}" for error in self.errors])
        string = f'{self.schema_name} :\n{errors}'
        return string


class UniqueGraphQLError(BaseError):
    name = 'UniqueError'

    def __init__(
            self,
            field: str | Iterable[str],
            value: str | Iterable[str],
            schema_name: str | None = None,
            path: list[str] | None = None,
            message: str | None = None,
    ):
        self.field = field
        self.value = value
        self.schema_name = schema_name
        self.message = message
        self._path = path

    def __str__(self) -> str:
        field = (
            f'({", ".join(map(str, self.field))})'
            if isinstance(self.field, Iterable)
            else self.field
        )
        value = (
            f'({", ".join(map(str, self.value))})'
            if isinstance(self.value, Iterable)
            else self.value
        )
        return self.message or f"Field '{field}' with value '{value}' already exists"

    @property
    def path(self):
        path = self._path or [
            self.schema_name,
            self.field
        ]
        return list(filter(lambda x: x, path))


class MultipleUniqueGraphQLErrors(MultipleExceptionsBase[UniqueGraphQLError]):
    def __str__(self) -> str:
        errors = '\n'.join([f"-\t{error}" for error in self.errors])
        string = f'UniqueExceptions :\n{errors}'
        return string


class NotFoundGraphQLError(BaseError):
    name = 'NotFoundError'

    def __init__(self, message: str, value: Any = None, path: list[str] = None):
        self.message = message
        self.value = value
        self.path = path or []

    def __str__(self):
        return self.message


class MultipleNotFoundGraphQLErrors(MultipleExceptionsBase[NotFoundGraphQLError]):
    pass
