from pydantic.main import ModelMetaclass, BaseModel
from typing import get_args
from copy import deepcopy


class ConfigMeta(ModelMetaclass):
    def __new__(mcs, name, bases, namespaces, **kwargs):
        config = namespaces.pop('HelperConfig', None)
        table = kwargs.pop('table', False)
        if config:
            bases = (super().__new__(mcs, name, bases, namespaces, **kwargs),)
            name, bases, namespaces, kwargs = mcs.configure(
                config, name, bases, namespaces, **kwargs
            )
        if table:
            kwargs['table'] = table
        if config:
            namespaces['Config'] = config
        return super().__new__(mcs, name, bases, namespaces, **kwargs)

    @classmethod
    def configure(mcs, config, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        fields = namespaces.get('__fields__', {})
        for base in bases:
            annotations.update(base.__annotations__)
            fields.update(base.__fields__)
        include = getattr(config, 'include', [])
        exclude = getattr(config, 'exclude', [])
        optional = getattr(config, 'optional', [])
        all_optional = getattr(config, 'all_optional', False)
        if include:
            annotations, fields = mcs.include_fields(
                include=include,
                annotations=annotations,
                fields=fields,
            )
        elif exclude:
            annotations, fields = mcs.exclude_fields(
                exclude=exclude,
                annotations=annotations,
                fields=fields
            )
        if optional or all_optional:
            annotations, fields = mcs.make_optional(
                optional=optional,
                annotations=annotations,
                fields=fields,
                all_optional=all_optional
            )
        namespaces['__annotations__'] = annotations
        namespaces['__fields__'] = fields
        return name, bases, namespaces, kwargs

    @classmethod
    def include_fields(
            mcs,
            include: list[str],
            annotations: dict,
            fields: dict,
    ) -> tuple[dict, dict]:
        merged_keys = fields.keys() & annotations.keys()
        [merged_keys.add(field) for field in fields]
        new_fields = {}
        new_annotations = {}
        for field in merged_keys:
            if not field.startswith('__') and field in include:
                new_annotations[field] = annotations.get(field, fields[field].type_)
                new_fields[field] = fields[field]
        return new_annotations, new_fields

    @classmethod
    def exclude_fields(
            mcs,
            exclude: list[str],
            annotations: dict,
            fields: dict,
    ) -> tuple[dict, dict]:
        merged_keys = fields.keys() & annotations.keys()
        [merged_keys.add(field) for field in fields]
        new_fields = {}
        new_annotations = {}
        for field in merged_keys:
            if not field.startswith('__') and field not in exclude:
                new_annotations[field] = annotations.get(field, fields[field].type_)
                new_fields[field] = fields[field]
        return new_annotations, new_fields

    @classmethod
    def make_optional(
            mcs,
            optional: list[str],
            annotations: dict,
            fields: dict,
            all_optional: bool = False
    ) -> tuple[dict, dict]:
        annotations = annotations.copy()
        merged_keys = fields.keys() & annotations.keys()
        new_annotations = {}
        new_fields = {}
        for field in merged_keys:
            if not field.startswith('__') and (all_optional or field in optional):
                type_ = annotations.get(field, fields[field].type_)
                if type(None) not in get_args(type_):
                    type_ = type_ | None
                new_annotations[field] = type_
                new_fields[field] = deepcopy(fields[field])
                new_fields[field].required = False
                if not (
                    new_fields[field].default
                    or new_fields[field].default_factory
                ):
                    new_fields[field].default = None

        return dict(annotations, **new_annotations), dict(fields, **new_fields)
