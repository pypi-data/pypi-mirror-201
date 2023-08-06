import asyncio
from quilt.vendors.GooglePlaces.main import Place, Address
from quilt.models.location import Location
from devtools import debug


async def get_place() -> Place:
    mad_green_place_id = "ChIJP5bmVaFZwokRyDdS3pPicdI"
    # invalid_place_id = mad_green_place_id[:-1] + "i"
    place = await Place.get(place_id=mad_green_place_id)
    assert place.place_id == mad_green_place_id
    return place


async def get_photos() -> None:
    place = await get_place()
    photo_urls = await place.get_photo_urls()
    print("photo_urls", photo_urls)
    assert len(photo_urls) > 1


async def main() -> None:
    # await get_photos()
    place = await get_place()
    debug(place)
    location = Location.from_place(place)
    debug(location)


if __name__ == "__main__":
    asyncio.run(main())
