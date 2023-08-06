from __future__ import annotations
import typing as T
from pydantic import BaseModel
from strawberry.types.types import TypeDefinition
from edge_orm import Node, Resolver
from quilt.vendors.Sentry.context_managers import span

NodeType = T.TypeVar("NodeType", bound=Node)
NodeTypeTemp = T.TypeVar("NodeTypeTemp", bound=Node)


class GQLUtilException(Exception):
    pass


def basemodel_to_straw(straw_cls: T.Type[StrawType], model: BaseModel) -> StrawType:
    """FUTURE check for speed, but for now it's like 1ms for small objs"""
    if model is None:
        raise GQLUtilException("model cannot be None")
    fields_to_fill = {
        f.name for f in straw_cls._type_definition.fields if f.base_resolver is None
    }
    d: dict[str, T.Any] = {}
    for field in fields_to_fill:
        d[field] = getattr(model, field)
    straw = straw_cls(**d)
    straw._node = model
    return straw


class classproperty(property):
    def __get__(self, owner_self: T.Any, owner_cls: T.Any) -> T.Any:  # type: ignore
        return self.fget(owner_cls)  # type: ignore


class StrawMixin(T.Generic[NodeType]):
    _node: NodeType
    _type_definition: TypeDefinition

    class Config:
        node_type: T.Type[NodeType]  # type: ignore
        resolver_type: T.Type[Resolver]

    @property
    def node(self) -> NodeType:
        return self._node

    @classmethod
    def from_node(
        cls: T.Type[StrawType], node: NodeType, use_span: bool = True
    ) -> StrawType:
        with span(op=f"from_node.{cls.__name__}", use=use_span):
            return basemodel_to_straw(straw_cls=cls, model=node)

    @classmethod
    def from_node_or_none(
        cls: T.Type[StrawType], node: NodeType | None, use_span: bool = True
    ) -> StrawType | None:
        if node is None:
            return None
        return cls.from_node(node=node, use_span=use_span)

    @classmethod
    def from_nodes(
        cls: T.Type[StrawType], nodes: list[NodeType], use_span: bool = True
    ) -> list[StrawType]:
        with span(
            op=f"from_nodes.{cls.__name__}",
            description=f"nodes count: {len(nodes)}",
            use=use_span,
        ):
            return [cls.from_node(node, use_span=use_span) for node in nodes]


StrawType = T.TypeVar("StrawType", bound=StrawMixin)  # type: ignore
