import typing as T
from ..strawberry_utils import StrawMixin
from .models import Preload, PreloadRaw, SkipTo
from . import helpers


class LogicException(Exception):
    pass


def preload_raw_to_preload(
    current_straw_type: T.Type[StrawMixin[T.Any]],
    preload_raw: PreloadRaw,
    actual_return_type: T.Any,
) -> Preload:
    # deal with return types first
    if preload_raw.return_type and preload_raw.path_to_return_type is None:
        raise LogicException(
            f"If return_type is provided, path_to_return_type must be provided. For {preload_raw.dict()=}."
        )
    if preload_raw.return_type:
        return_type = helpers.return_type_from_return_annotation(
            raw_return_type=preload_raw.return_type,
            current_straw_type=current_straw_type,
        )
    else:
        return_type = actual_return_type
    skip_to = SkipTo(
        return_type=return_type,
        path_to_return_type=preload_raw.path_to_return_type or [],
    )
    if preload_raw.update_resolver_f:
        update_resolver_f = preload_raw.update_resolver_f
        update_resolver_f_given = True
    else:
        update_resolver_f = preload_raw.update_rez
        update_resolver_f_given = False

    return Preload(
        update_resolver_f=update_resolver_f,
        update_resolver_f_given=update_resolver_f_given,
        skip_to=skip_to,
        fields_to_include=preload_raw.fields_to_include or set(),
        permissions=preload_raw.permissions,
    )
