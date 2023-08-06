from typing import Generic, TypeVar, Iterable

import strawberry

GenericType = TypeVar('GenericType')


@strawberry.type
class PageInfo:
    has_next_page: bool = strawberry.field(
        description="When paginating forwards, are there more items?"
    )
    has_previous_page: bool = strawberry.field(
        description="When paginating backwards, are there more items?"
    )
    start_cursor: str | None = strawberry.field(
        description="When paginating backwards, the cursor to continue."
    )
    end_cursor: str | None = strawberry.field(
        description="When paginating forwards, the cursor to continue."
    )


@strawberry.type
class Edge(Generic[GenericType]):
    node: GenericType = strawberry.field(
        description="The item at the end of the edge."
    )
    cursor: str = strawberry.field(
        description="A cursor for use in pagination."
    )


@strawberry.type
class Connection(Generic[GenericType]):
    page_info: PageInfo = strawberry.field(
      description="Information to aid in pagination."
    )

    edges: list[Edge[GenericType]] = strawberry.field(
      description="A list of edges in this connection."
    )

    def __init__(
            self,
            nodes: Iterable[GenericType],
            cursor_name: str,
            first: int,
            after: str | None = None,
    ):
        edges = [
            Edge(
                cursor=getattr(node, cursor_name),
                node=node
            )
            for node in nodes
        ]
        has_next_page = len(edges) == first
        if has_next_page:
            edges = edges[:-1]
        self.page_info = PageInfo(
            has_next_page=has_next_page,
            has_previous_page=after is not None,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if edges else None
        )
        self.edges = edges

