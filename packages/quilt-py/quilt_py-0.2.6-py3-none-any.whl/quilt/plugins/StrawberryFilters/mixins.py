import typing as T
from pydantic import BaseModel
from edge_orm import Resolver
from dataclasses import asdict

if T.TYPE_CHECKING:
    from .default_filters import (
        AddToResolverMixin,
        AddToResolverMixinOrder,
    )

ThisResolverType = T.TypeVar("ThisResolverType", bound=Resolver)


class FilterMixin:
    def filter_obj(
        self: ThisResolverType,
        filter: T.Union["AddToResolverMixin", BaseModel, dict[str, T.Any]],
    ) -> ThisResolverType:
        from . import logic
        from app.dbs.edgedb.gen import filters

        if not filter:
            return self
        if not isinstance(filter, BaseModel):
            if not isinstance(filter, dict):
                filter = asdict(filter)
            filter = filters.FilterOrderByName["Filter" + self.model_name](**filter)

        filter_str, variables = logic.node_filter_to_str(f=filter, root_field_name="")
        return self.filter(filter_str, variables)

    def order_obj(
        self: ThisResolverType,
        order: T.Union["AddToResolverMixinOrder", BaseModel, dict[str, T.Any]],
    ) -> ThisResolverType:
        from . import logic
        from app.dbs.edgedb.gen import filters

        if not order:
            return self
        if not isinstance(order, BaseModel):
            if not isinstance(order, dict):
                order = asdict(order)
            order = filters.FilterOrderByName["Order" + self.model_name](**order)

        order_str = logic.order_to_str(order)
        return self.order_by(order_str)
