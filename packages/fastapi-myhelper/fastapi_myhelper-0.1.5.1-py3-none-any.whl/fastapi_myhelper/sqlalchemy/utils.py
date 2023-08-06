from sqlalchemy.orm.attributes import InstrumentedAttribute


def attrs_name_equality(first_attr, second_attr) -> bool:
    first_attr_name = (
        first_attr.property.key
        if isinstance(first_attr, InstrumentedAttribute)
        else first_attr.key
    )
    second_attr_name = (
        second_attr.property.key
        if isinstance(second_attr, InstrumentedAttribute)
        else second_attr.key
    )
    return first_attr_name == second_attr_name
