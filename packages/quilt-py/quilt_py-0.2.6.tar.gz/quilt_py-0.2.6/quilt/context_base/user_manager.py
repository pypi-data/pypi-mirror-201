import typing as T
import edge_orm
from fastapi import Request
from functools import cached_property
from edgedb import AsyncIOClient
from pydantic import BaseModel, Field, EmailStr
from quilt import DisplayException, logs
from quilt.vendors.Firebase import auth
from edge_orm import UNSET, UnsetType

logger = logs.create_logger(__name__)


class Identities(BaseModel):
    # apple.com -> array of apple ids
    apple_com: list[str] | None = Field(None, alias="apple.com")
    email: list[str] | None = None


class Firebase(BaseModel):
    sign_in_provider: str  # apple.com for apple or password for email
    identities: Identities


class InvalidAuthHeader(DisplayException):
    pass


class AuthExpirationException(DisplayException):
    pass


class AuthTokenPayload(BaseModel):
    name: str | None = None  # for apple this will exist, for email this will not
    iss: str
    aud: str
    auth_time: int
    user_id: str
    sub: str
    iat: int
    exp: int
    email: EmailStr | None = None
    email_verified: bool | None = None
    # firebase: Firebase # not used now so don't want to spend time parsing
    phone_number: str | None = None

    @classmethod
    def from_token_firebase(cls, bearer_token: str | bytes) -> "AuthTokenPayload":
        try:
            raw_jwt = auth.verify_id_token(bearer_token)
        except auth.InvalidIdTokenError as e:
            logger.debug(f"{e=}")
            if "Token expired" in str(e):
                raise AuthExpirationException(str(e))
            raise InvalidAuthHeader(str(e))
        return cls(**raw_jwt)


class UserManagerException(Exception):
    pass


UserType = T.TypeVar("UserType", bound=edge_orm.Node)
UserResolverType = T.TypeVar("UserResolverType", bound=edge_orm.Resolver)


class UserMixin(T.Generic[UserType, UserResolverType]):
    def __init__(
        self,
        default_resolver_function: T.Callable[[], UserResolverType],
        default_include_properties_function: T.Callable[[UserResolverType], None],
        auth_id_field_name: T.Optional[str] = "auth_id",
    ):
        self.default_resolver_function = default_resolver_function
        self.default_include_properties_function = default_include_properties_function
        self.auth_id_field_name = auth_id_field_name

    request: Request
    _user: UserType | None | UnsetType

    @property
    def auth_header(self) -> str | None:
        return self.request.headers.get("Authorization")

    @cached_property
    def jwt_user(self) -> AuthTokenPayload | None:
        auth_header = self.auth_header
        if not auth_header:
            return None
        try:
            [auth_kind, token] = auth_header.split(" ")
        except ValueError:
            logger.error(f"invalid auth header: {auth_header}END")
            raise InvalidAuthHeader("Invalid Authorization Header", traces_rate=0.1)
        return AuthTokenPayload.from_token_firebase(token)

    @property
    def auth_id(self) -> str | None:
        if not self.jwt_user:
            return None
        return self.jwt_user.user_id

    @property
    def admin_auth_id(self) -> str | None:
        # FUTURE when doing admin on behalf of...
        return None

    async def get(
        self,
        given_resolver: T.Optional[UserResolverType] = None,
        *,
        refresh: T.Optional[bool] = False,
        include_properties: T.Optional[bool] = True,
        include_permissions: T.Optional[bool] = True,
        client: T.Optional[AsyncIOClient] = None,
    ) -> UserType | None:
        if refresh:
            self._user = UNSET
        if self._user is not UNSET:
            return self._user
        if not self.auth_id:
            return None
        resolver = given_resolver or self.default_resolver_function()
        if include_properties:
            self.default_include_properties_function(resolver)
        if include_permissions:
            resolver.include_fields("permissions")
        self._user = await resolver.get(
            **{self.auth_id_field_name: self.auth_id, "client": client}
        )
        return self._user

    async def gerror(
        self,
        given_resolver: T.Optional[UserResolverType] = None,
        *,
        refresh: T.Optional[bool] = False,
        include_properties: T.Optional[bool] = True,
        include_permissions: T.Optional[bool] = True,
        client: T.Optional[AsyncIOClient] = None,
    ) -> UserType | None:
        try:
            return await self.get(
                given_resolver=given_resolver,
                refresh=refresh,
                include_properties=include_properties,
                include_permissions=include_permissions,
                client=client,
            )
        except edge_orm.ResolverException:
            raise UserManagerException("Please create an account to access.")

    def set(self, user: UserType | None) -> None:
        self._user = user
