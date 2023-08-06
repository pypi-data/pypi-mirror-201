import typing as T
from datetime import datetime
from zoneinfo import ZoneInfo
import strawberry
from strawberry.unset import UnsetType


@strawberry.interface
class InputDateTimeInterface:
    day: int
    month: int
    year: int
    hour: int
    minute: int

    def to_datetime(self, tz: ZoneInfo) -> datetime:
        return datetime(
            day=self.day,
            month=self.month,
            year=self.year,
            hour=self.hour,
            minute=self.minute,
            tzinfo=tz,
        )

    @classmethod
    def from_datetime(
        cls, dt: datetime, zone_info: ZoneInfo
    ) -> "InputDateTimeInterface":
        dt = dt.astimezone(tz=zone_info)
        return cls(
            day=dt.day, month=dt.month, year=dt.year, hour=dt.hour, minute=dt.minute
        )


@strawberry.input
class InputDateTime(InputDateTimeInterface):
    pass

    @staticmethod
    def to_datetime_or_none(
        input: T.Union["InputDateTime", None, UnsetType], tz: ZoneInfo
    ) -> datetime | None | UnsetType:
        if isinstance(input, InputDateTime):
            return input.to_datetime(tz)
        return input


@strawberry.type
class InputDateTimeDisplay(InputDateTimeInterface):
    pass
