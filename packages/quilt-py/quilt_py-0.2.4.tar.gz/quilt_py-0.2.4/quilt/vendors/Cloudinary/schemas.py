from datetime import datetime
from pydantic import AnyHttpUrl, BaseModel


class CloudinaryImage(BaseModel):
    asset_id: str
    bytes: int | None = None
    created_at: datetime
    etag: str | None = None
    format: str
    height: int
    width: int
    original_filename: str | None = None
    pages: int | None = None
    phash: str | None = None
    placeholder: str | None = None
    public_id: str
    resource_type: str
    secure_url: AnyHttpUrl | None = None
    signature: str | None = None
    tags: list[str] | None = None
    type: str | None = None
    url: AnyHttpUrl
    version: int
    version_id: str | None = None
