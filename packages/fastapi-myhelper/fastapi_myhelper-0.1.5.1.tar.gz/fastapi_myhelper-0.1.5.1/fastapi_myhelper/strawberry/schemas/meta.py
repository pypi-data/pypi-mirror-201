import inspect
import dataclasses
from typing import Any, Type, get_args, TypeVar
from copy import copy

import strawberry
from strawberry.object_type import StrawberryField
from strawberry.type import StrawberryOptional


class TypeMeta(type):
    def __new__(mcs, name, bases, namespaces, **kwargs):
        is_schema = kwargs.pop('pydantic_schema', None)
        save_point = kwargs.pop('__save_point', None)
        if is_schema:
            bases = (type(name, bases, namespaces, **kwargs, __save_point=True),)
        config = namespaces.get('Config', None) or (
            getattr(bases[0], 'Config', None)
            if bases else None
        )
        if config and not is_schema and not save_point:
            (
                config,
                name,
                bases,
                namespaces,
                kwargs
            ) = mcs.configurate(
                mcs=mcs,
                config=config,
                name=name,
                bases=bases,
                namespaces=namespaces,
                **kwargs
            )
        kls = super().__new__(mcs, name, bases, namespaces, **kwargs)
        mcs.set_validators(kls=kls)
        return kls

    def configurate(mcs, config, name, bases, namespaces, **kwargs):
        namespaces = namespaces.copy()
        optional = getattr(config, 'optional', None)
        defaults = getattr(config, 'defaults', None)
        if optional:
            fields, annotations = mcs.make_optional(
                bases=bases,
                namespaces=namespaces,
                **optional,
            )
            namespaces = dict(namespaces, **fields)
            namespaces['__annotations__'] = dict(
                getattr(namespaces, '__annotations__', {}),
                **annotations
            )
        if defaults:
            fields = mcs.make_defaults(
                namespaces=namespaces,
                defaults=defaults,
            )
            namespaces = dict(namespaces, **fields)
        return (
            config,
            name,
            bases,
            namespaces,
            kwargs
        )

    @staticmethod
    def make_optional(
            bases: tuple[Type[type]],
            namespaces: dict[str, Any],
            fields: list[str] | None = None,
            all_fields: bool = False,
    ) -> tuple[
        dict[str, StrawberryField],
        dict[str, Any],
    ]:
        kls_fields = {}
        fields_to_proccess = {}
        annotations = {}
        for base in bases:
            annotations.update(inspect.get_annotations(base))
            for base_ in base.mro():
                fields_to_proccess.update(base_.__dict__)
        fields_to_proccess.update(namespaces.copy())
        annotations.update(namespaces.get('__annotations__', {}))
        for field_name in annotations:
            if not all_fields and field_name not in fields:
                continue
            if getattr(annotations, field_name, None) == strawberry.auto:
                continue
            kls_fields[field_name] = strawberry.UNSET
            if type(None) not in get_args(annotations[field_name]):
                annotations[field_name] = annotations[field_name] | None
        return (
            kls_fields,
            annotations
        )

    @staticmethod
    def make_defaults(
            namespaces: dict[str, Any],
            defaults: dict[str, Any],
    ) -> dict[str, Any]:
        result = {}
        non_listed = set(defaults.keys()) - set(namespaces.keys())
        if non_listed:
            raise ValueError(
                f'Attributes ({", ".join(non_listed)}) doesn\'t exists'
            )
        for key in defaults:
            result[key] = defaults[key]
        return result

    @staticmethod
    def set_validators(kls):
        kls.__validators__ = list(filter(
            lambda x: getattr(x, '__validator_config__', None),
            [
                method[1]
                for method in inspect.getmembers(kls, predicate=inspect.ismethod)
            ]
        ))
