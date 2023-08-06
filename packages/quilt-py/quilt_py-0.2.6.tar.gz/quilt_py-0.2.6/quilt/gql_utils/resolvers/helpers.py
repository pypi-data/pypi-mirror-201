import typing as T
import types
from edge_orm import Node
from app import helpers
from ..strawberry_utils import StrawMixin
from strawberry.types.nodes import SelectedField, FragmentSpread, InlineFragment


StrawType = T.TypeVar("StrawType", bound=StrawMixin[Node])


class ResolverUtilException(Exception):
    pass


def base_type_from_return_type(return_type: T.Any) -> T._AnnotatedAlias | None:  # type: ignore
    if isinstance(return_type, T._AnnotatedAlias):  # type: ignore
        return return_type
    if isinstance(return_type, (T._UnionGenericAlias, types.UnionType)):  # type: ignore
        args = T.get_args(return_type)
        for a in args:
            if base_type := base_type_from_return_type(a):
                return base_type
    if isinstance(return_type, (T.GenericAlias, T._GenericAlias)):  # type: ignore
        return T.get_args(return_type)[0]
    return None


def return_type_or_str_from_return_annotation(return_annotation: T.Any) -> T.Any:
    """Unpacks annotation if forward-looking"""
    while isinstance(return_annotation, T.GenericAlias):  # type: ignore
        return_annotation = T.get_args(return_annotation)[0]
    if "Annotated[ForwardRef" in str(return_annotation):
        annotated_return_type = base_type_from_return_type(return_annotation)
        if not annotated_return_type:
            raise Exception(
                f"Invalid return_type: {return_annotation=}, {type(return_annotation)}"
            )
        args = T.get_args(annotated_return_type)
        abc = args[1].resolve_forward_ref(args[0])
        return abc.resolve_type()
    return return_annotation


def return_type_from_return_annotation(
    raw_return_type: T.Any, current_straw_type: T.Type[StrawType]
) -> T.Any:
    return_type = return_type_or_str_from_return_annotation(
        return_annotation=raw_return_type
    )
    if isinstance(return_type, str) and (
        return_type == current_straw_type.__name__
        or f"['{current_straw_type.__name__}']" in str(return_type)
    ):
        return current_straw_type
    if isinstance(return_type, str):
        raise Exception(f"Return type cannot be str but is: {return_type=}.")
    return return_type


def selected_field_from_path(
    top_field: SelectedField, path: list[str]
) -> SelectedField:
    for part in path:
        part = helpers.snake_to_camel(part)
        found_part = False
        selections = top_field.selections.copy()
        for sel in selections:
            if isinstance(sel, (FragmentSpread, InlineFragment)):
                selections.extend(sel.selections)
                continue
            if sel.name == part:
                top_field = sel
                found_part = True
                break
        if found_part is False:
            message = f"{part=} not in {top_field.selections}"
            raise ResolverUtilException(message)
    return top_field
