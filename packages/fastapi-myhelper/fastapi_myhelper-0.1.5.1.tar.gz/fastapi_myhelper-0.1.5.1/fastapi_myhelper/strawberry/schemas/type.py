from typing import Iterable, Callable

from .meta import TypeMeta
from ..exceptions import (
    ValidationError,
    MultipleValidationErrors
)


class TypeBase(metaclass=TypeMeta):
    """class configuration
    class Config:
        pydantic_schema: bool = False
        optional: dict = {
            "all_field": True / False - Makes all fields optional,
            "fields": list[str] - Makes selected fields optional
        }
        defaults: dict = {
            field_name: field_default - set default values for specific fields
        }
    """
    __validators__ = []

    def __post_init__(self):
        self.validate()

    @property
    def name(self):
        return self._type_definition.name

    @classmethod
    @property
    def validators(cls):
        return cls.__validators__

    def validate(self):
        errors = []
        for validator in self.__validators__:
            config = validator.__validator_config__
            fields = {
                field: getattr(self, field)
                for field in config.get('fields', None)
            } if not config.get('all_fields', False) else {
                field: value
                for field, value in self.__dict__.items()
            }
            try:
                validator(**fields)
            except ValidationError as e:
                errors.append(e)
        if errors:
            raise MultipleValidationErrors(
                *errors,
                schema_name=self.name
            )



