import httpx
from pydantic import BaseModel
from quilt.vendors.GooglePlaces.main import Place, Address
from quilt import DisplayException

TZ_FROM_COORDS_URL = (
    "https://getzipcodeinfo.herokuapp.com/get_tz_from_coords?lat=<LAT>&lng=<LNG>"
)


class LocationError(DisplayException):
    pass


def tz_from_coords(lat: float, lng: float) -> str:
    url = TZ_FROM_COORDS_URL.replace("<LAT>", str(lat)).replace("<LNG>", str(lng))
    return httpx.get(url).json()


class Location(BaseModel):
    lat: float
    lng: float
    city: str | None = None
    state_abbr: str | None = None
    country_name: str | None = None
    postal_code: str | None = None
    street_address: str | None = None

    formatted_address: str | None = None

    timezone: str
    place_id: str

    @classmethod
    def from_place(cls, place: Place) -> "Location":
        address = Address.from_place(place)
        loc = place.geometry.location
        return cls(
            lat=loc.lat,
            lng=loc.lng,
            city=address.city,
            state_abbr=address.state_abbr,
            country_name=address.country_name,
            postal_code=address.postal_code,
            street_address=address.street_address,
            formatted_address=place.formatted_address,
            timezone=tz_from_coords(lat=loc.lat, lng=loc.lng),
            place_id=place.place_id,
        )

    @classmethod
    async def from_place_id(
        cls, place_id: str, force_street_address: bool = True
    ) -> "Location":
        place = await Place.get(place_id=place_id)
        loc = cls.from_place(place)
        if force_street_address and not loc.street_address:
            raise LocationError(
                "Street Address required but not given. Please choose a location with a street address."
            )
        return loc


import strawberry


@strawberry.experimental.pydantic.type(model=Location, name="Location", all_fields=True)
class LocationStraw:
    pass


@strawberry.experimental.pydantic.input(
    model=Location, name="LocationInput", all_fields=True
)
class LocationStrawInput:
    pass
