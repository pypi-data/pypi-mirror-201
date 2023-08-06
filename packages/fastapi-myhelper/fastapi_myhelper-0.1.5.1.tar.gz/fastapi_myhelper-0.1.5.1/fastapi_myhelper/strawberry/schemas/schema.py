from strawberry import Schema as BaseSchema
from strawberry.utils.logging import StrawberryLogger
from strawberry.types import ExecutionContext
from graphql.error import GraphQLError


class Schema(BaseSchema):
    __excluded_exception = ()

    def process_errors(
        self,
        errors: list[GraphQLError],
        execution_context: ExecutionContext | None = None,
    ) -> None:
        for error in errors:
            if isinstance(error.original_error, self.__excluded_exception):
                continue
            StrawberryLogger.error(
                error=error,
                execution_context=execution_context
            )

    def exclude_exceptions(self, *exceptions):
        self.__excluded_exception = exceptions

    # async def execute( # TODO sometime later create atomic transactions
    #     self,
    #     *args, **kwargs
    # ):
    #     context = kwargs.get('context_value')
    #     result = await super().execute(*args, **kwargs)
    #     if result.errors:
    #         await context.session.rollback()
    #     else:
    #         await context.session.commit()
    #     return result

