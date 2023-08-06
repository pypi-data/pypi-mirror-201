import typing as T
import functools
import inspect
from enum import Enum
from pydantic import BaseModel
from edge_orm import Resolver, Node
from edge_orm.types_generator.main import COUNT_POSTFIX
from ..strawberry_utils import StrawMixin
from strawberry.types.nodes import SelectedField
from app import helpers


NodeType = T.TypeVar("NodeType", bound=Node)
REZ_FUNC = T.Callable[..., T.Union[Resolver, T.Awaitable[Resolver]]]
UPDATED_REZ_FUNC = T.Callable[
    ..., T.Union[Resolver, T.Awaitable[Resolver], None, T.Awaitable[None]]
]
Func = T.TypeVar("Func", bound=T.Callable[..., T.Any])


def kwargs_from_selected_field(
    rez_function: T.Callable[..., T.Any],
    selected_field: SelectedField,
    auth_id: str | None,
) -> dict[str, T.Any]:
    params = inspect.signature(rez_function).parameters
    kwargs = {helpers.camel_to_snake(k): v for k, v in selected_field.arguments.items()}
    if "_auth_id" in params and "_auth_id" not in kwargs:
        kwargs["_auth_id"] = auth_id
    if "_child_field" in params and "_child_field" not in kwargs:
        kwargs["_child_field"] = selected_field
    return kwargs


class PreloadRaw(BaseModel):
    field_name: str
    update_resolver_f: T.Callable[..., T.Any] | None = None
    return_type: T.Any | None = None
    path_to_return_type: list[str] | None = None
    fields_to_include: set[str] | None = None
    alias: str | None = None
    rez_function: T.Callable[..., T.Any] | None = None
    permissions: set[Enum] | None = None

    def only_fields_to_include(self) -> bool:
        return {"field_name", "fields_to_include"} == self.dict(
            exclude_none=True
        ).keys()

    async def update_rez(
        self,
        rez: Resolver,
        selected_field: SelectedField,
        return_type: T.Type[StrawMixin[NodeType]] | T.Any,
        auth_id: str = None,
    ) -> Resolver | None:
        """Assuming update_resolver_f does not exist"""
        """returns none if first_name and only including fields"""
        """returns resolver if return type is a straw mixin"""
        has_count_postfix = self.field_name.endswith(COUNT_POSTFIX)
        if self.update_resolver_f:
            raise Exception("update_resolver_f already exists, just use that.")
        if self.fields_to_include:
            rez.include_fields(*self.fields_to_include)
        if (
            not (inspect.isclass(return_type) and issubclass(return_type, StrawMixin))
            and not self.rez_function
            and not has_count_postfix
        ):
            return None
        edge_name = self.alias or self.field_name
        if self.rez_function:
            kwargs = kwargs_from_selected_field(
                rez_function=self.rez_function,
                selected_field=selected_field,
                auth_id=auth_id,
            )
            nested_rez = self.rez_function(**kwargs)
            if inspect.isawaitable(nested_rez):
                nested_rez = await nested_rez
        else:
            nested_rez = return_type.Config.resolver_type()
            if has_count_postfix:
                nested_rez.is_count = True
        result = getattr(rez, edge_name)(nested_rez)
        if inspect.isawaitable(result):
            await result
        return nested_rez


class SkipTo(BaseModel):
    return_type: T.Any
    path_to_return_type: list[str]


class Preload(BaseModel):
    """
    update_resolver_f can be null in cases where you just want to go to return type

    skip_to only given if return type is Straw or if you should 'continue'.
    Otherwise, you can stop following this trail.
    """

    update_resolver_f: T.Callable[..., T.Any] | None
    update_resolver_f_given: bool

    skip_to: SkipTo
    fields_to_include: set[str]
    permissions: set[Enum] | None


def preload(
    *,
    update_resolver_f: UPDATED_REZ_FUNC = None,
    return_type: T.Any = None,
    path_to_return_type: list[str] = None,
    fields_to_include: set[str] = None,
    alias: str = None,
    rez_function: REZ_FUNC = None,
    permissions: T.Optional[set[Enum]] = None
) -> T.Callable[[Func], Func]:
    def inner(func: Func) -> Func:
        preload_raw = PreloadRaw(
            field_name=func.__name__,
            update_resolver_f=update_resolver_f,
            return_type=return_type,
            path_to_return_type=path_to_return_type,
            fields_to_include=fields_to_include,
            alias=alias,
            rez_function=rez_function,
            permissions=permissions,
        )
        if "raw_preloads" not in func.__dict__:
            func.__dict__["raw_preloads"] = []
        func.__dict__["raw_preloads"].append(preload_raw)
        return func

    return inner


def is_count(func):  # type: ignore
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):  # type: ignore
        rez = func(*args, **kwargs)
        if inspect.isawaitable(rez):
            rez = await rez
        rez.is_count = True
        return rez

    return wrapper
