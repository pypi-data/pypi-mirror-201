import os
import typing as T
import httpx
from pydantic import BaseModel
from quilt.errors import DisplayException

BASE_URL = "https://maps.googleapis.com/maps/api/place"

google_places_api_key = os.environ["GOOGLE_PLACES_API_KEY"]


class GooglePlacesException(Exception):
    pass


class GooglePlacesExceptionDisplay(DisplayException):
    pass


class Component(BaseModel):
    long_name: str
    short_name: str
    types: list[str]


class Point(BaseModel):
    lat: float
    lng: float


class Viewport(BaseModel):
    northeast: Point
    southwest: Point


class Geometry(BaseModel):
    location: Point
    viewport: Viewport


class Photo(BaseModel):
    photo_reference: str
    height: int
    width: int
    html_attributions: list[str]


class Address(BaseModel):
    street_address: str | None = None
    city: str | None = None
    state_abbr: str | None = None
    postal_code: str | None = None
    country_name: str | None = None

    @classmethod
    def from_place(cls, place: "Place") -> T.Optional["Address"]:
        if not place.adr_address:
            return None
        chunks = place.adr_address.split('<span class="')
        d = {}
        for chunk in chunks:
            if not chunk:
                continue
            try:
                label = chunk[: chunk.index('"')]
                value = chunk[chunk.index(">") + 1 : chunk.index("<")]
                d[label] = value
            except ValueError as e:
                print(f"Error With Location {e=}, {chunk=}")
        return cls(
            street_address=d.get("street-address"),
            city=d.get("locality"),
            state_abbr=d.get("region"),
            postal_code=d.get("postal-code"),
            country_name=d.get("country-name"),
        )


class Place(BaseModel):
    address_components: list[Component]
    adr_address: str
    formatted_address: str
    geometry: Geometry
    icon: str
    icon_background_color: str
    icon_mask_base_uri: str
    name: str
    photos: list[Photo] = []
    place_id: str
    reference: str
    url: str
    utc_offset: int
    vicinity: str

    _endpoint: T.ClassVar[str] = BASE_URL + "/details/json?"
    _photos_endpoint: T.ClassVar[str] = BASE_URL + "/photo"

    @classmethod
    async def get(cls, place_id: str) -> "Place":
        async with httpx.AsyncClient() as client:
            response = await client.get(
                cls._endpoint,
                params={"place_id": place_id, "key": google_places_api_key},
            )
        data = response.json()
        if data["status"] == "INVALID_REQUEST":
            raise GooglePlacesExceptionDisplay(
                f"The place you are looking for was not found: place_id {place_id} not found."
            )
        return Place(**data["result"])

    async def get_photo_urls(self) -> list[str]:
        """returns google urls of the photos"""
        urls: list[str] = []
        async with httpx.AsyncClient() as client:
            for photo in self.photos:
                response = await client.get(
                    self._photos_endpoint,
                    params={
                        "photo_reference": photo.photo_reference,
                        "key": google_places_api_key,
                        "maxwidth": photo.width,
                        "maxheight": photo.height,
                    },
                )
                if response.status_code != 302:
                    raise GooglePlacesException(
                        f"Invalid photo reference: {photo.photo_reference=}"
                    )
                urls.append(response.headers["location"])
        return urls
