import os
import time
import httpx
import functools
from pydantic import BaseModel


base_url = "https://ipinfo.io"


class IpInfoResponse(BaseModel):
    ip: str
    hostname: str | None = None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    loc: str | None = None
    org: str | None = None
    postal: str | None = None
    timezone: str | None = None
    bogon: bool | None = None

    def get_location(self) -> str:
        if not self.city and not self.region and not self.country:
            return "Local Request"
        return f"{self.city}, {self.region} in {self.country}"


@functools.lru_cache(maxsize=1_000)
def get_ip_info(ip_address: str) -> IpInfoResponse | None:
    if not ip_address:
        return None
    res = httpx.get(f"{base_url}/{ip_address}?token={os.environ['IP_INFO_TOKEN']}")
    if res.status_code == 200:
        return IpInfoResponse(**res.json())
    return None


if __name__ == "__main__":
    start = time.time()
    print(get_ip_info(ip_address="51.91.31.157").get_location())  # type: ignore
    print(time.time() - start)
