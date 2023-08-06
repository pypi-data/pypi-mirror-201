from graphql import GraphQLError
from strawberry.extensions import (
    Extension,
    MaskErrors as BaseMaskErrors,
)
from typing import Type, Iterable, Callable, Any

from ..exceptions import BaseError


__all__ = [
    'MaskErrors',
    'ErrorHandler'
]


def default_format_error(error: BaseError, prev_path: list[str]) -> GraphQLError:
    return GraphQLError(
        str(error),
        original_error=error,
        path=[*prev_path, *getattr(error, 'path', [])],
        extensions={
            'type': error.name,
            'value': getattr(error, 'value', None)
        }
    )


class ErrorHandler(Extension):
    def __init__(
            self,
            exclude: tuple[Type[Extension]],
            format_error: Callable[[...], GraphQLError]
    ):
        self.exclude = exclude,
        self.format_error = default_format_error

    def on_executing_end(self):
        result = self.execution_context.result
        if not result or not result.errors:
            return
        processed_errors = []
        for error in result.errors:
            original_error = error.original_error
            if not (
                error.original_error
                and isinstance(original_error, self.exclude)
            ):
                processed_errors.append(error)
                continue

            if isinstance(original_error, Iterable):
                processed_errors.extend(map(
                    lambda nested_error: self.format_error(
                        error=nested_error,
                        prev_path=error.path
                    ), original_error
                ))
            else:
                processed_errors.append(self.format_error(
                    error=original_error,
                    prev_path=error.path
                ))

        result.errors = processed_errors


class MaskErrors(BaseMaskErrors):
    def __init__(
            self, *,
            exclude: tuple[Type[Extension]],
            error_message: str = "Unexpected error.",
    ):
        self.exclude = exclude
        self.error_message = error_message

    def should_mask_error(self, error: GraphQLError) -> bool:
        original_error = error.original_error
        if original_error and isinstance(
            original_error,
            self.exclude
        ):
            return False
        return True

