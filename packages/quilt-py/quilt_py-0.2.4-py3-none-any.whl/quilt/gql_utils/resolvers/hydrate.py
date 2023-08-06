import typing as T
import inspect
from enum import Enum
from strawberry.type import StrawberryList
from strawberry.union import StrawberryUnion
from strawberry.types.nodes import SelectedField, FragmentSpread, InlineFragment
from quilt.gql_utils.strawberry_utils import StrawMixin
from quilt.gql_utils.resolvers.models import Preload, kwargs_from_selected_field
from edge_orm import Resolver
from app.api import Info
from quilt import helpers, logs
from .helpers import selected_field_from_path, ResolverUtilException

logger = logs.create_logger(__name__)

StrawType = T.TypeVar("StrawType", bound=StrawMixin[T.Any])
ResolverType = T.TypeVar("ResolverType", bound=Resolver)


async def update_rez(
    rez: Resolver,
    straw_type: T.Type[StrawType],
    selected_field: SelectedField,
    auth_id: str | None,
) -> set[Enum]:
    """this should return a set of all permissions found"""
    permissions: set[Enum] = set()
    selections = selected_field.selections.copy()
    while selections:
        child_field = selections.pop(0)
        if isinstance(child_field, (FragmentSpread, InlineFragment)):
            selections.extend(child_field.selections)
            continue
        child_field_name = helpers.camel_to_snake(child_field.name)
        if child_field_name in rez._node_config.node_edgedb_conversion_map:
            rez.include_fields(child_field_name)
        # find the function on the straw_type
        straw_field: T.Callable[..., T.Any] | None = getattr(
            straw_type, child_field_name, None
        )
        if straw_field is None:
            # Non strawberry_field fields; for example, 'id' field. Already included so move on.
            continue
        if preloads := straw_field.__dict__.get("preloads"):
            preloads = T.cast(list[Preload], preloads)
            for preload in preloads:
                if preload.permissions:
                    permissions.update(preload.permissions)
                if not preload.update_resolver_f_given:
                    nested_rez = preload.update_resolver_f(
                        rez=rez,
                        selected_field=child_field,
                        return_type=preload.skip_to.return_type,
                        auth_id=auth_id,
                    )
                else:
                    kwargs = kwargs_from_selected_field(
                        rez_function=preload.update_resolver_f,
                        selected_field=child_field,
                        auth_id=auth_id,
                    )
                    nested_rez = preload.update_resolver_f(rez=rez, **kwargs)
                    if preload.fields_to_include:
                        rez.include_fields(*preload.fields_to_include)
                if inspect.isawaitable(nested_rez):
                    nested_rez = await nested_rez
                if nested_rez:
                    if preload.skip_to.path_to_return_type:
                        try:
                            child_field = selected_field_from_path(
                                top_field=child_field,
                                path=preload.skip_to.path_to_return_type,
                            )
                        except ResolverUtilException:
                            continue
                    nested_permissions = await update_rez(
                        rez=nested_rez,
                        straw_type=preload.skip_to.return_type,
                        selected_field=child_field,
                        auth_id=auth_id,
                    )
                    permissions.update(nested_permissions)
    return permissions


def straw_type_from_union(union: StrawberryUnion) -> T.Type[StrawType]:
    straw_type = None
    for t in union.types:
        if issubclass(t, StrawMixin):
            if straw_type is not None:
                raise Exception(
                    "There is more than one straw type in the union "
                    "so you must specify which one with the `return_straw_type` field."
                )
            straw_type = t
    if not straw_type:
        raise Exception("There is no straw type in the response union.")
    return straw_type


async def rez_from_info(
    info: Info,
    return_straw_type: T.Optional[T.Type[StrawType]] = None,
    path_to_nested_field: T.Optional[list[str]] = None,
) -> ResolverType:
    return_straw_type = return_straw_type or info.return_type
    if isinstance(return_straw_type, StrawberryList):
        return_straw_type = return_straw_type.of_type  # type: ignore
    return_straw_type = T.cast(T.Type[StrawType], return_straw_type)
    if isinstance(return_straw_type, StrawberryUnion):
        return_straw_type = straw_type_from_union(return_straw_type)
    rez = return_straw_type.Config.resolver_type()
    top_field = info.selected_fields[0]
    if path_to_nested_field:
        top_field = selected_field_from_path(
            top_field=top_field, path=path_to_nested_field
        )
    permissions = await update_rez(
        rez=rez,
        straw_type=return_straw_type,
        selected_field=top_field,
        auth_id=info.context.auth.auth_id,
    )
    permissions.update(info.context.permissions)
    # now turn permissions into has_permissions_str
    if permissions:
        inner_str = [
            f"<{str(p).split('.')[0]}>'{p.value}' in global current_user.permissions"
            for p in permissions
        ]
        rez.has_permission_str_ = " and ".join(inner_str)
        print(f"{rez.has_permission_str_=}")
    return rez
