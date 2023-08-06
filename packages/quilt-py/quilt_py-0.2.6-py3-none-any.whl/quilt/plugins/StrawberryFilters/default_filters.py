import typing as T
import datetime
from enum import Enum
from pydantic import BaseModel, Field, root_validator
import strawberry
import edge_orm
from edge_orm import UNSET, UnsetType
import sentry_sdk
from dataclasses import dataclass, asdict


def to_lower_camel(string: str) -> str:
    return "".join(
        word.capitalize() if i != 0 else word
        for i, word in enumerate(string.split("_"))
    )


class ParseFilterMixin(BaseModel):
    @root_validator(pre=True)
    def none_to_unset(cls, values: dict[str, T.Any]) -> dict[str, T.Any]:
        """For some reason on some nested fields, strawberry sends a None, not an UNSET. So much amke sure all
        Nones are not given, therefore defaulting to UNSET as set in the pydantic object.
        """
        return {k: v for k, v in values.items() if v is not None}

    @classmethod
    def from_filter(
        cls: T.Type["FilterPydanticType"], filter: dict[str, T.Any]
    ) -> "FilterPydanticType":
        """techincally also takes in strawberry input but can't find the type for this..."""
        if type(filter) is dict:
            d = filter
        else:
            d = asdict(filter)
            # d = {k: None if v is UNSET else v for k, v in d.items()}
        # TURN Nones into UNSETS -> idk why straw has this
        # d = {k: v for k, v in d.items() if v is not None} # this did not solve it
        node = cls.parse_obj(d)
        return node

    def add_filter_to_resolver(self, resolver: edge_orm.Resolver) -> None:
        from .logic import node_filter_to_str

        with sentry_sdk.start_span(
            op="Add Filter to Resolver", description=f"{resolver.__class__.__name__}"
        ):
            filter_str, variables = node_filter_to_str(f=self, root_field_name="")
            resolver.filter(filter_str, variables)

    def add_order_to_resolver(self, resolver: edge_orm.Resolver) -> None:
        from .logic import order_to_str

        with sentry_sdk.start_span(
            op="Add Order to Resolver", description=f"{resolver.__class__.__name__}"
        ):
            order_str = order_to_str(self)
            resolver.order_by(order_str)

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


FilterPydanticType = T.TypeVar("FilterPydanticType", bound=ParseFilterMixin)


class FilterString(ParseFilterMixin):
    in_: list[str] | UnsetType = Field(
        alias="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[str] | UnsetType = UNSET
    exists: bool | UnsetType = UNSET
    eq: str | UnsetType = UNSET
    neq: str | UnsetType = UNSET
    gte: str | UnsetType = UNSET
    gt: str | UnsetType = UNSET
    lte: str | UnsetType = UNSET
    lt: str | UnsetType = UNSET
    like: str | UnsetType = UNSET
    ilike: str | UnsetType = UNSET


@strawberry.experimental.pydantic.input(model=FilterString, name="FilterString")
class FilterStringStraw:
    in_: list[str] | None = strawberry.field(
        name="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[str] | None = UNSET
    exists: bool | None = UNSET
    eq: str | None = UNSET
    neq: str | None = UNSET
    gte: str | None = UNSET
    gt: str | None = UNSET
    lte: str | None = UNSET
    lt: str | None = UNSET
    like: str | None = UNSET
    ilike: str | None = UNSET


class FilterDateTime(FilterString):
    pass


FilterDateTimeStraw = strawberry.experimental.pydantic.input(
    model=FilterDateTime, name="FilterDateTime"
)(FilterStringStraw)


class FilterDate(ParseFilterMixin):
    in_: list[datetime.date] | UnsetType = Field(
        alias="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[datetime.date] | UnsetType = UNSET
    exists: bool | UnsetType = UNSET
    eq: datetime.date | UnsetType = UNSET
    neq: datetime.date | UnsetType = UNSET
    gte: datetime.date | UnsetType = UNSET
    gt: datetime.date | UnsetType = UNSET
    lte: datetime.date | UnsetType = UNSET
    lt: datetime.date | UnsetType = UNSET


@strawberry.experimental.pydantic.input(model=FilterDate, name="FilterDate")
class FilterDateStraw:
    in_: list[datetime.date] | None = strawberry.field(
        name="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[datetime.date] | None = UNSET
    exists: bool | None = UNSET
    eq: datetime.date | None = UNSET
    neq: datetime.date | None = UNSET
    gte: datetime.date | None = UNSET
    gt: datetime.date | None = UNSET
    lte: datetime.date | None = UNSET
    lt: datetime.date | None = UNSET


class FilterTime(ParseFilterMixin):
    in_: list[datetime.time] | UnsetType = Field(
        alias="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[datetime.time] | UnsetType = UNSET
    exists: bool | UnsetType = UNSET
    eq: datetime.time | UnsetType = UNSET
    neq: datetime.time | UnsetType = UNSET
    gte: datetime.time | UnsetType = UNSET
    gt: datetime.time | UnsetType = UNSET
    lte: datetime.time | UnsetType = UNSET
    lt: datetime.time | UnsetType = UNSET


@strawberry.experimental.pydantic.input(model=FilterTime, name="FilterTime")
class FilterTimeStraw:
    in_: list[datetime.time] | None = strawberry.field(
        name="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[datetime.time] | None = UNSET
    exists: bool | None = UNSET
    eq: datetime.time | None = UNSET
    neq: datetime.time | None = UNSET
    gte: datetime.time | None = UNSET
    gt: datetime.time | None = UNSET
    lte: datetime.time | None = UNSET
    lt: datetime.time | None = UNSET


class FilterJSON(FilterString):
    pass


FilterJSONStraw = strawberry.experimental.pydantic.input(
    model=FilterJSON, name="FilterJSON"
)(FilterStringStraw)


class FilterID(ParseFilterMixin):
    in_: list[str] | UnsetType = Field(
        alias="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[str] | UnsetType = UNSET
    exists: bool | UnsetType = UNSET
    eq: str | UnsetType = UNSET
    neq: str | UnsetType = UNSET


@strawberry.experimental.pydantic.input(model=FilterID, name="FilterID")
class FilterIDStraw:
    in_: list[str] | None = strawberry.field(
        name="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[str] | None = UNSET
    exists: bool | None = UNSET
    eq: str | None = UNSET
    neq: str | None = UNSET


class FilterInt(ParseFilterMixin):
    in_: list[int] | UnsetType = Field(
        alias="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[int] | UnsetType = UNSET
    exists: bool | UnsetType = UNSET
    eq: int | UnsetType = UNSET
    neq: int | UnsetType = UNSET
    gte: int | UnsetType = UNSET
    gt: int | UnsetType = UNSET
    lte: int | UnsetType = UNSET
    lt: int | UnsetType = UNSET


@strawberry.experimental.pydantic.input(model=FilterInt, name="FilterInt")
class FilterIntStraw:
    in_: list[int] | None = strawberry.field(
        name="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[int] | None = UNSET
    exists: bool | None = UNSET
    eq: int | None = UNSET
    neq: int | None = UNSET
    gte: int | None = UNSET
    gt: int | None = UNSET
    lte: int | None = UNSET
    lt: int | None = UNSET


class FilterInt16(FilterInt):
    pass


FilterInt16Straw = strawberry.experimental.pydantic.input(
    model=FilterInt16, name="FilterInt16"
)(FilterIntStraw)


class FilterInt32(FilterInt):
    pass


FilterInt32Straw = strawberry.experimental.pydantic.input(
    model=FilterInt32, name="FilterInt32"
)(FilterIntStraw)


class FilterInt64(FilterInt):
    pass


FilterInt64Straw = strawberry.experimental.pydantic.input(
    model=FilterInt64, name="FilterInt64"
)(FilterIntStraw)


class FilterFloat(ParseFilterMixin):
    in_: list[float] | UnsetType = Field(
        alias="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[float] | UnsetType = UNSET
    exists: bool | UnsetType = UNSET
    eq: float | UnsetType = UNSET
    neq: float | UnsetType = UNSET
    gte: float | UnsetType = UNSET
    gt: float | UnsetType = UNSET
    lte: float | UnsetType = UNSET
    lt: float | UnsetType = UNSET


@strawberry.experimental.pydantic.input(model=FilterFloat, name="FilterFloat")
class FilterFloatStraw:
    in_: list[float] | None = strawberry.field(
        name="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[float] | None = UNSET
    exists: bool | None = UNSET
    eq: float | None = UNSET
    neq: float | None = UNSET
    gte: float | None = UNSET
    gt: float | None = UNSET
    lte: float | None = UNSET
    lt: float | None = UNSET


class FilterFloat16(FilterFloat):
    pass


FilterFloat16Straw = strawberry.experimental.pydantic.input(
    model=FilterFloat16, name="FilterFloat16"
)(FilterFloatStraw)


class FilterFloat32(FilterFloat):
    pass


FilterFloat32Straw = strawberry.experimental.pydantic.input(
    model=FilterFloat32, name="FilterFloat32"
)(FilterFloatStraw)


class FilterFloat64(FilterFloat):
    pass


FilterFloat64Straw = strawberry.experimental.pydantic.input(
    model=FilterFloat64, name="FilterFloat64"
)(FilterFloatStraw)


class FilterBoolean(ParseFilterMixin):
    in_: list[bool] | UnsetType = Field(
        alias="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[bool] | UnsetType = UNSET
    exists: bool | UnsetType = UNSET
    eq: bool | UnsetType = UNSET
    neq: bool | UnsetType = UNSET


@strawberry.experimental.pydantic.input(model=FilterBoolean, name="FilterBoolean")
class FilterBooleanStraw:
    in_: list[bool] | None = strawberry.field(
        name="in", default_factory=lambda: strawberry.UNSET
    )
    nin: list[bool] | None = UNSET
    exists: bool | None = UNSET
    eq: bool | None = UNSET
    neq: bool | None = UNSET


class DirectionEnum(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


strawberry.enum(DirectionEnum)


class NullsOrderingEnum(str, Enum):
    SMALLEST = "SMALLEST"
    BIGGEST = "BIGGEST"


strawberry.enum(NullsOrderingEnum)


class Ordering(ParseFilterMixin):
    dir: DirectionEnum
    nulls: NullsOrderingEnum | UnsetType = NullsOrderingEnum.SMALLEST


@strawberry.input(name="Ordering")
class OrderingStraw:
    dir: DirectionEnum
    nulls: NullsOrderingEnum | None = NullsOrderingEnum.SMALLEST


class FromDictMixin:
    pass
    """
    def to_pydantic(self) -> FilterPydanticType:
        return self.Config.pydantic_type.parse_obj(asdict(self))
    """


class AddToResolverMixin(FromDictMixin):
    def add_to_resolver(self, resolver: edge_orm.Resolver) -> None:
        from .logic import node_filter_to_str

        with sentry_sdk.start_span(
            op="Add Filter to Resolver", description=f"{resolver.__class__.__name__}"
        ):
            filter_str, variables = node_filter_to_str(f=self, root_field_name="")
            resolver.filter(filter_str, variables)


class AddToResolverMixinOrder(FromDictMixin):
    def add_to_resolver(self, resolver: edge_orm.Resolver) -> None:
        from .logic import order_to_str

        with sentry_sdk.start_span(
            op="Add Order to Resolver", description=f"{resolver.__class__.__name__}"
        ):
            resolver.order_by(order_to_str(self))
