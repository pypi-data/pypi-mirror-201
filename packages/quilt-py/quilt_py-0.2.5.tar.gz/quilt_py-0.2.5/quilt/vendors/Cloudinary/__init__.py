import typing as T
import os
import sys
import re
from retry_async import retry
from . import schemas as S

from cloudinary.exceptions import Error as CloudinaryError
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name=os.environ["CLOUDINARY_CLOUD_NAME"],
    api_key=os.environ["CLOUDINARY_API_KEY"],
    api_secret=os.environ["CLOUDINARY_SECRET_KEY"],
)


def get_public_id_from_url(url: str) -> str | None:
    patt = "v\d*\/(.*)\."
    ids = re.findall(pattern=patt, string=url)
    if not ids or not len(ids):
        return None
    return ids[0]


def get_image(image_id: str) -> S.CloudinaryImage:
    resource = cloudinary.api.resource(image_id, phash=True)
    resource["url"] = resource.get("secure_url")
    return S.CloudinaryImage(**resource)


@retry(CloudinaryError, tries=5, delay=1, is_async=False)
def upload_image(url_or_bytes: T.Union[bytes, str]) -> S.CloudinaryImage:
    size = sys.getsizeof(url_or_bytes)
    print("size of url or bytes", size)
    res = cloudinary.uploader.upload(
        url_or_bytes, phash=True, folder=os.environ["CLOUDINARY_FOLDER_NAME"]
    )
    return S.CloudinaryImage(**res)
