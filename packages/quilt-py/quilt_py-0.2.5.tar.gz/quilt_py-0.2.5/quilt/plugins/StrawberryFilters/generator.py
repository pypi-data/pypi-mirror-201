import re
import typing as T
import types
from enum import Enum
from pathlib import Path
from black import format_str, FileMode
import edge_orm
from edge_orm.types_generator.main import stringify_dict

"""NODES"""

NodeType = T.TypeVar("NodeType", bound=T.Type[edge_orm.Node])


cast_to_python_filter_name = {
    "std::uuid": "FilterID",
    "std::str": "FilterString",
    "std::json": "FilterJSON",
    "std::datetime": "FilterDateTime",
    "cal::local_date": "FilterDate",
    "cal::local_time": "FilterTime",
    "std::bool": "FilterBoolean",
    "std::int16": "FilterInt16",
    "std::int32": "FilterInt32",
    "std::int64": "FilterInt64",
    "std::float16": "FilterFloat16",
    "std::float32": "FilterFloat32",
    "std::float64": "FilterFloat64",
}

python_filter_name_to_cast = {
    val: key for key, val in cast_to_python_filter_name.items()
}


def import_str() -> str:
    lst = [
        "from __future__ import annotations",
        "import strawberry",
        "from edge_orm import UnsetType, UNSET",
        "from pydantic import Field",
    ]
    return "\n".join(lst)


def indent_lines(s: str, indent: str = "    ") -> str:
    chunks = s.split("\n")
    return indent + f"\n{indent}".join(chunks)


def build_filter_str_from_node(node_cls: NodeType) -> str:
    fields: dict[str, str] = {}
    print(f"node_cls: {node_cls}")
    for field_name, val in node_cls.EdgeConfig.node_edgedb_conversion_map.items():
        cast = val.base_cast or val.cast
        if filter_str := cast_to_python_filter_name.get(cast):
            fields[field_name] = filter_str
        else:
            # check if enum
            if cast.startswith("default::"):
                enum_name = cast.split("::")[-1]
                fields[field_name] = f"Filter{enum_name}"
            else:
                print("NO MATCH", f"{field_name=}, {cast=}")
                # array<str>... worry about this later
                pass

    # now for links
    for link_name, val in node_cls.EdgeConfig.insert_link_conversion_map.items():
        fields[link_name] = f"NestedFilter{val.cast}"

    field_strs: list[str] = []
    field_strs_straw: list[str] = []
    for field_name, filter_str_val in fields.items():
        field_strs.append(f"{field_name}: {filter_str_val} | UnsetType = UNSET")
        field_strs_straw.append(f"{field_name}: {filter_str_val}Straw | None = UNSET")
    all_fields_str = "\n".join(field_strs)
    all_fields_str_straw = "\n".join(field_strs_straw)

    filter_name = f"Filter{node_cls.__name__}"
    filter_name_straw = f"{filter_name}Straw"
    root_filter = f"""
class {filter_name}(ParseFilterMixin):
    and_: list[{filter_name}] | UnsetType = Field(strawberry.UNSET, alias="and")
    or_: list[{filter_name}] | UnsetType = Field(strawberry.UNSET, alias="or")
    not_: {filter_name} | UnsetType = Field(strawberry.UNSET, alias="not")
{indent_lines(all_fields_str)}


@strawberry.input(name="{filter_name}")
class {filter_name_straw}(AddToResolverMixin):
    and_: list[{filter_name_straw}] | None = strawberry.field(name="and", default_factory=lambda: strawberry.UNSET)
    or_: list[{filter_name_straw}] | None = strawberry.field(name="or", default_factory=lambda: strawberry.UNSET)
    not_: {filter_name_straw} | None = strawberry.field(name="not", default_factory=lambda: strawberry.UNSET)
{indent_lines(all_fields_str_straw)}
    
    class Config:
        pydantic_type = {filter_name}
    """

    nested_filter_name = f"Nested{filter_name}"
    nested_filter_name_straw = f"{nested_filter_name}Straw"

    nested_filter = f"""

class {nested_filter_name}(ParseFilterMixin):
    exists: bool | UnsetType = UNSET
{indent_lines(all_fields_str)}

@strawberry.input(name="{nested_filter_name}")
class {nested_filter_name_straw}:
    exists: bool | None = UNSET
{indent_lines(all_fields_str_straw)}

    class Config:
        pydantic_type = {nested_filter_name}
    """

    order_strs: list[str] = []
    order_strs_straw: list[str] = []
    for field_name, filter_str_val in fields.items():
        ordering_str = "Ordering"
        if filter_str_val.startswith("NestedFilter"):
            ordering_str = "Order" + filter_str_val.split("NestedFilter")[-1]
        order_strs.append(f"{field_name}: {ordering_str} | UnsetType = UNSET")
        order_strs_straw.append(f"{field_name}: {ordering_str}Straw | None = UNSET")

    all_order_str = "\n".join(order_strs)
    all_order_str_straw = "\n".join(order_strs_straw)

    order_name = f"Order{node_cls.__name__}"
    order_name_straw = f"{order_name}Straw"

    order_str = f"""
class {order_name}(ParseFilterMixin):
{indent_lines(all_order_str)}

@strawberry.input(name="{order_name}")
class {order_name_straw}(AddToResolverMixinOrder):
{indent_lines(all_order_str_straw)}

    class Config:
        pydantic_type = {order_name}
    """

    return root_filter + "\n" + nested_filter + "\n" + order_str


def build_node_str(nodes: list[T.Type[edge_orm.Node]]) -> str:
    strs = [build_filter_str_from_node(node) for node in nodes]
    # now do forward refs too
    node_str = "\n".join(strs)
    pattern = "class (\w+)\(ParseFilterMixin\):"
    class_names = re.findall(pattern, node_str)
    print(f"{class_names=}")
    ref_lst: list[str] = [f"{name}.update_forward_refs()" for name in class_names]
    return node_str + "\n" + "\n".join(ref_lst)


def build_node_str_from_module(module: types.ModuleType) -> str:
    unique_nodes = unique_nodes_from_module(module)
    s = build_node_str(unique_nodes)
    return format_str(s, mode=FileMode())


def unique_nodes_from_module(module: types.ModuleType) -> list[T.Type[edge_orm.Node]]:
    node_vals: list[T.Type[edge_orm.Node]] = []
    for d in dir(module):
        val = getattr(module, d)
        try:
            if issubclass(val, edge_orm.Node) and hasattr(val, "EdgeConfig"):
                node_vals.append(val)
        except TypeError:
            pass
    # dedup, take the last one imported
    seen_nodes_by_name: dict[str, T.Type[edge_orm.Node]] = {}
    unique_nodes: set[T.Type[edge_orm.Node]] = set()
    for node in node_vals:
        if seen_node := seen_nodes_by_name.get(node.__name__):
            if issubclass(seen_node, node):
                continue
            else:
                unique_nodes.remove(seen_node)
        seen_nodes_by_name[node.__name__] = node
        unique_nodes.add(node)
    return sorted(list(unique_nodes), key=lambda x: x.__name__)


"""ENUMS"""


def build_filter_str_from_enum(e: T.Type[Enum]) -> str:
    if e.__name__ == "Enum":
        return ""
    enum_name = f"enums.{e.__name__}"
    model_name = f"Filter{e.__name__}"
    model_name_straw = f"{model_name}Straw"
    return f"""
class {model_name}(ParseFilterMixin):
    in_: list[{enum_name}] | UnsetType = Field(alias="in", default_factory=lambda: strawberry.UNSET)
    nin: list[{enum_name}] | UnsetType = UNSET
    exists: bool | UnsetType = UNSET
    eq: {enum_name} | UnsetType = UNSET
    neq: {enum_name} | UnsetType = UNSET
    gte: {enum_name} | UnsetType = UNSET
    gt: {enum_name} | UnsetType = UNSET
    lte: {enum_name} | UnsetType = UNSET
    lt: {enum_name} | UnsetType = UNSET

@strawberry.input(name="{model_name}")
class {model_name_straw}:
    in_: list[{enum_name}] | None = strawberry.field(name="in", default_factory=lambda: strawberry.UNSET)
    nin: list[{enum_name}] | None = UNSET
    exists: bool | None = UNSET
    eq: {enum_name} | None = UNSET
    neq: {enum_name} | None = UNSET
    gte: {enum_name} | None = UNSET
    gt: {enum_name} | None = UNSET
    lte: {enum_name} | None = UNSET
    lt: {enum_name} | None = UNSET
"""


def build_enum_str(enums: list[T.Type[Enum]]) -> str:
    print(f"{enums=}")
    strs = [build_filter_str_from_enum(e) for e in enums]
    return "\n".join(strs)


def build_enum_str_from_module(module: types.ModuleType) -> str:
    enum_vals: list[T.Type[Enum]] = []
    for d in dir(module):
        val = getattr(module, d)
        try:
            if issubclass(val, Enum):
                enum_vals.append(val)
        except TypeError:
            pass
    s = build_enum_str(sorted(list(set(enum_vals)), key=lambda x: x.__name__))
    return format_str(s, mode=FileMode())


class GeneratorException(Exception):
    pass


def build_default_filters_path_import_str(default_filters_import_path: str) -> str:
    if not default_filters_import_path.endswith(".default_filters"):
        raise GeneratorException(
            "default_filters_import_path must end with `.default_filters`"
        )
    imports = [
        "ParseFilterMixin",
        "AddToResolverMixin",
        "AddToResolverMixinOrder",
        "FromDictMixin",
        "FilterID",
        "FilterIDStraw",
        "FilterDateTime",
        "FilterDateTimeStraw",
        "FilterJSON",
        "FilterJSONStraw",
        "FilterString",
        "FilterStringStraw",
        "FilterBoolean",
        "FilterBooleanStraw",
        "FilterInt64",
        "FilterInt64Straw",
        "FilterInt16",
        "FilterInt16Straw",
        "FilterInt32",
        "FilterInt32Straw",
        "FilterFloat16",
        "FilterFloat16Straw",
        "FilterFloat32",
        "FilterFloat32Straw",
        "FilterFloat64",
        "FilterFloat64Straw",
        "Ordering",
        "OrderingStraw",
        "DirectionEnum",
        "NullsOrderingEnum",
    ]
    return f"from {default_filters_import_path} import {', '.join(imports)}"


def generate_filters(
    enums_module: types.ModuleType,
    db_module: types.ModuleType,
    default_filters_import_path: str,
    output_path: Path,
    enums_path: str,
) -> None:
    enums_s = build_enum_str_from_module(enums_module)
    nodes_s = build_node_str_from_module(db_module)

    # update forward refs for these nodes -> so get all classes and update the forward refs
    class_names = re.findall("class (\w+)\(", nodes_s)
    non_straw_class_names = [c for c in class_names if not c.endswith("Straw")]
    update_forward_refs_str = "\n".join(
        [f"{c}.update_forward_refs()" for c in non_straw_class_names]
    )

    mapping = {f"{c}": c for c in non_straw_class_names}
    mapping_str = "FilterOrderByName: dict[str, ParseFilterMixin] = " + stringify_dict(
        mapping, stringify_value=False
    )

    strs = [
        import_str(),
        build_default_filters_path_import_str(default_filters_import_path),
        enums_path,
        enums_s,
        nodes_s,
        update_forward_refs_str,
        mapping_str,
    ]
    s = format_str("\n".join(strs), mode=FileMode())
    with open(output_path, "w") as output_file:
        output_file.write(s)


def main() -> None:
    from app.dbs import enums, db

    generate_filters(
        enums,
        db,
        "from app.plugins.StrawberryFilters.default_filters import *",
        Path("app/app/dbs/edgedb/gen/filters.py"),
        enums_path="from app.dbs import enums",
    )


if __name__ == "__main__":
    main()
