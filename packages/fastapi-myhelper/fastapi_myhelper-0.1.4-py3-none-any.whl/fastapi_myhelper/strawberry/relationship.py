import strawberry
from strawberry.lazy_type import (
    LazyType as InitialLazyType,
    StrawberryLazyReference as InitialStrawberryLazyReference
)
from strawberry.utils.str_converters import to_camel_case
from dataclasses import dataclass
from typing import ForwardRef, Annotated, Type


@dataclass(frozen=True)
class LazyType(InitialLazyType):
    back_populates: str | None = None

    def resolve_type(self) -> Type:
        kls = super().resolve_type()
        kls = strawberry.type(
            type(
                self.create_name(kls=kls),
                (kls,), dict(kls.__dict__)
            ),
            is_input=kls._type_definition.is_input,
            is_interface=kls._type_definition.is_interface,
            description=kls._type_definition.description,
            directives=kls._type_definition.directives,
            extend=kls._type_definition.extend
        )
        kls.__dataclass_fields__.pop(self.back_populates)
        for field_idx in range(len(kls._type_definition._fields)):
            if kls._type_definition._fields[field_idx].name == self.back_populates:
                kls._type_definition._fields.pop(field_idx)
                break
        return kls

    def create_name(self, kls):
        return f"{kls._type_definition.name}{to_camel_case(self.back_populates.capitalize())}Rel"


class StrawberryLazyReference(InitialStrawberryLazyReference):
    def __init__(self, *args, back_populates: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.back_populates = back_populates

    def resolve_forward_ref(self, forward_ref: ForwardRef) -> LazyType:
        return LazyType(
            forward_ref.__forward_arg__,
            self.module,
            self.package,
            self.back_populates
        )


def Relationship(
        name: str,
        module_path: str,
        back_populates: str,
) -> StrawberryLazyReference:
    return Annotated[
        name,
        StrawberryLazyReference(module_path, back_populates=back_populates)
    ]