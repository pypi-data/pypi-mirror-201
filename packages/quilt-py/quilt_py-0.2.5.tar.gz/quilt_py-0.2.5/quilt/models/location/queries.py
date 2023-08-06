import strawberry
from . import LocationStraw, Location
from app import permissions


@strawberry.type
class LocationQuery:
    @strawberry.field(permission_classes=[permissions.Authed])
    async def location(self, place_id: str) -> LocationStraw:
        return LocationStraw.from_pydantic(
            await Location.from_place_id(place_id=place_id)
        )
