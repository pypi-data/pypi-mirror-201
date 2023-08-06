import typing

import dateutil.parser
from pydantic import BaseModel
from strawberry import UNSET
from .default_filters import (
    NullsOrderingEnum,
    Ordering,
    OrderingStraw,
    AddToResolverMixin,
    AddToResolverMixinOrder,
)
from .generator import python_filter_name_to_cast
from devtools import debug


class FilterException(Exception):
    pass


filter_field_to_edb_operation = {
    "eq": "=",
    "neq": "!=",
    "gte": ">=",
    "gt": ">",
    "lte": "<=",
    "lt": "<",
    "like": "like",
    "ilike": "ilike",
}


def order_to_str(order: AddToResolverMixinOrder | BaseModel, path: str = "") -> str:
    parts: list[str] = []
    # d = order.dict() if isinstance(order, BaseModel) else order.__dict__
    d = order.__dict__

    for field_name, val in d.items():
        if val is not UNSET:
            if isinstance(val, Ordering) or isinstance(val, OrderingStraw):
                empty_val = ""
                if val.nulls == NullsOrderingEnum.BIGGEST:
                    empty_val = " EMPTY LAST"
                parts.append(f"{path}.{field_name} {val.dir.value.lower()}{empty_val}")
            else:
                # this is a nested order
                parts.append(order_to_str(val, path=f"{path}.{field_name}"))
    if not parts:
        return ""
    return " THEN ".join(parts)


VARS = dict[str, str]
PARTS_VARS = tuple[str, VARS]


def scalar_filter_to_str(
    f: AddToResolverMixin | BaseModel, root_field_name: str
) -> PARTS_VARS:
    filter_name = f.__class__.__name__
    value_cast = python_filter_name_to_cast.get(filter_name)
    is_enum = False
    if not value_cast:
        value_cast = filter_name[6:]
        is_enum = True

    # d = f.dict() if isinstance(f, BaseModel) else f.__dict__
    d = f.__dict__

    set_d = {k: v for k, v in d.items() if v is not UNSET}
    parts: list[str] = []
    variables: VARS = {}
    for field_name, val in set_d.items():
        use_val = True
        # val_var_name = (root_field_name + field_name + random_str(8)).replace(".", "")
        val_var_name = (root_field_name + field_name).replace(
            ".", ""
        )  # TODO test if this works
        if value_cast == "std::datetime" and type(val) is str:
            val = dateutil.parser.parse(val)
        if field_name in ["in_", "nin"]:
            if field_name == "in_":
                in_or_nin = "IN"
            elif field_name == "nin":
                in_or_nin = "NOT IN"
            else:
                raise Exception(f"must be in_ or nin, is {field_name=}")
            if not is_enum:
                part = f"{root_field_name} {in_or_nin} <{value_cast}>array_unpack(<array<str>>${val_var_name})"
            else:
                part = f"{root_field_name} {in_or_nin} <{value_cast}>array_unpack(<array<str>>${val_var_name})"
        elif field_name == "exists":
            part = f"{'NOT ' if val is False else ''}EXISTS .{root_field_name}"
            use_val = False
        elif operation := filter_field_to_edb_operation.get(field_name):
            part = f".{root_field_name} {operation} <{value_cast}>${val_var_name}"
        else:
            raise FilterException(f"Unknown filter name, {field_name=}, {filter=}")
        parts.append(part)
        if use_val:
            variables[val_var_name] = val
    return " AND ".join(parts).replace("..", "."), variables


def node_filter_to_str(
    f: AddToResolverMixin | BaseModel, root_field_name: str
) -> PARTS_VARS:
    # d = f.dict() if isinstance(f, BaseModel) else f.__dict__
    d = f.__dict__
    return dict_to_filter_and_vars(d, root_field_name=root_field_name)


def dict_to_filter_and_vars(
    d: dict[str, typing.Any], root_field_name: str
) -> tuple[str, dict[str, typing.Any]]:
    variables: VARS = {}
    or_part: str = ""
    and_part: str = ""
    normal_parts: list[str] = []

    set_d = {k: v for k, v in d.items() if v is not UNSET}
    for field_name, val in set_d.items():
        # print(f"{field_name=}, {val=}")
        # if this is a scalar (enum or default, not nested filter)
        if field_name in ["or_", "and_"]:
            nested_parts: list[str] = []
            for nested_filter in val:
                nested_part, nested_vs = node_filter_to_str(
                    f=nested_filter, root_field_name=root_field_name
                )
                if nested_part:
                    nested_parts.append(nested_part)
                    variables.update(nested_vs)
            if field_name == "or_":
                join_str = "OR"
                part = ", ".join([f"({p})" for p in nested_parts])
                part = f"any({{ {part} }})"
            else:
                # Note: could do all() the same way you do any() above. The reason not to do this
                # is because it might actually be desired for AND the way it is -> if empty, make whole thing empty
                join_str = "AND"
                part = f" {join_str} ".join([f"({p})" for p in nested_parts])
                part = f"({part})"
            if len(set_d) > 1:
                part = f"{join_str} {part}"
            if part:
                if field_name == "or_":
                    or_part = part
                else:
                    and_part = part
        elif field_name == "not_":
            part, vs = node_filter_to_str(f=val, root_field_name=root_field_name)
            if part:
                normal_parts.append(f"NOT ({part})")
                variables.update(vs)
        elif field_name == "exists":
            rf = f".{root_field_name}".replace("..", ".")
            s = f"EXISTS {rf}"
            if val is False:
                s = f"NOT {s}"
            normal_parts.append(s)
        else:
            new_root_field_name = f"{root_field_name}.{field_name}"
            if val.__class__.__name__.startswith("NestedFilter"):
                part, vs = node_filter_to_str(
                    f=val, root_field_name=new_root_field_name
                )
                normal_parts.append(part)
                variables.update(vs)
            else:
                part, vs = scalar_filter_to_str(
                    f=val, root_field_name=new_root_field_name
                )
                normal_parts.append(part)
                variables.update(vs)

    normal_str = " AND ".join(normal_parts)
    final_str = f"{normal_str} {and_part} {or_part}"
    final_str = " ".join(final_str.split())

    return final_str, variables
