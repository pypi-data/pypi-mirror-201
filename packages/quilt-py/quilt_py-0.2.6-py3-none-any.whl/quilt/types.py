import strawberry


@strawberry.type
class NotFound:
    get_by_value: str | None = None
    message: str | None = "Not found."


@strawberry.type
class InvalidPermissions:
    get_by_value: str | None = None
    message: str | None = "You do not have permissions."
