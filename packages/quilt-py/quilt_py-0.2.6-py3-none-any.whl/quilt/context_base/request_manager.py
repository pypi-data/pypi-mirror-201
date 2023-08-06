import typing as T
from fastapi import Request
from starlette.requests import URL  # type: ignore


class RequestMixin:
    request: Request

    def get_header_from_list(
        self, name: str, first_val: T.Optional[bool] = True
    ) -> str | None:
        arr = self.request.headers.get(name)
        if arr:
            if not first_val:
                return arr
            return arr.split(",")[-1]
        return None

    @property
    def user_agent(self) -> str | None:
        return self.request.headers.get("user-agent")

    @property
    def x_forwarded_for(self) -> str | None:
        return self.get_header_from_list("x-forwarded-for")

    @property
    def cf_connecting_ip(self) -> str | None:
        return self.get_header_from_list("cf-connecting-ip")

    @property
    def ip_address(self) -> str | None:
        if cf_ip := self.cf_connecting_ip:
            return cf_ip
        if ip := self.x_forwarded_for:
            return ip
        return self.request.client.host

    @property
    def url(self) -> URL:
        return self.request.url

    @property
    def url_used(self) -> str:
        return str(self.url)


class RequestManagerException(Exception):
    pass


class RequestManager(RequestMixin):
    def __init__(self, request: Request):
        if request is None:
            raise RequestManagerException("Request cannot be None.")
        self.request = request
