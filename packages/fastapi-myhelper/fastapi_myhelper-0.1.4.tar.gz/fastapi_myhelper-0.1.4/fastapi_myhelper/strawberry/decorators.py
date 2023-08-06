from typing import Callable


def validator(
        *fields: str,
        all_fields: bool = False
):
    if not any([fields, all_fields]):
        raise ValueError('No one field is present')

    def __decorator(method: Callable):
        kls_method = classmethod(method)
        setattr(
            method,
            '__validator_config__',
            {
                'fields': fields,
                'all_fields': all_fields
            }
        )
        return kls_method
    return __decorator
