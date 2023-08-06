import typing as T
from pydantic import BaseModel
import strawberry
from enum import Enum


class VerticalAlign(str, Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


class Image(BaseModel):
    height: int
    width: int
    url: str
    public_cloudinary_id: str
    vertical_align: VerticalAlign | None = None


strawberry.enum(VerticalAlign)


@strawberry.experimental.pydantic.type(model=Image, name="Image", all_fields=True)
class ImageStraw:
    pass


@strawberry.experimental.pydantic.input(model=Image, name="ImageInput", all_fields=True)
class ImageStrawInput:
    pass


class SmallImage(BaseModel):
    url: str
    public_cloudinary_id: T.Optional[str] = None
    height: T.Optional[int] = None
    width: T.Optional[int] = None


@strawberry.experimental.pydantic.type(
    model=SmallImage, name="SmallImage", all_fields=True
)
class SmallImageStraw:
    pass
