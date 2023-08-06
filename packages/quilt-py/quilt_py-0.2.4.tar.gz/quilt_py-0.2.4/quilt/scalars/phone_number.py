import typing as T
import strawberry
from quilt.models.phone_number import PhoneNumber as PN

PhoneNumber = strawberry.scalar(
    T.NewType("PhoneNumber", PN),
    description="Phone number.",
    serialize=lambda v: v,
    parse_value=lambda v: PN.validate(v),
)
