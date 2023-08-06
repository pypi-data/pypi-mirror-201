import typing as T
import random
import string
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from edge_orm import UNSET, CHANGES
from devtools import pformat
from pydantic import BaseModel


def random_str(n: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


def random_str_digits(n: int) -> str:
    return "".join(random.choices(string.digits, k=n))


def operation_name_from_query(q: str) -> str:
    pattern = r"(query|mutation)\s+(\w+)"
    if matches := re.findall(pattern, q):
        return matches[0][1]
    else:
        q = "".join(q.split())
        return q[:20]


NYC_TZ = ZoneInfo("America/New_York")

DEFAULT_TZ = ZoneInfo("America/New_York")


def nyc() -> datetime:
    return datetime.now(tz=NYC_TZ)


def is_value(v: T.Any) -> bool:
    if v is UNSET:
        return False
    if v is None:
        return False
    return True


def camel_to_snake(s: str) -> str:
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def snake_to_camel(s: str) -> str:
    temp = s.split("_")
    return temp[0] + "".join(ele.title() for ele in temp[1:])


def pretty_str(val: T.Any, tz: T.Optional[ZoneInfo] = None) -> str:
    tz = tz or DEFAULT_TZ
    if isinstance(val, str):
        try:
            val = datetime.fromisoformat(val)
        except ValueError:
            pass
    if isinstance(val, datetime):
        return val.astimezone(tz=tz).strftime("%m/%d/%Y %-I:%M%p %Z")
    if isinstance(val, BaseModel):
        return pformat(val)
    return str(val)


def pretty_price(price: float | int) -> str:
    return f"${price:,.2f}".replace(".00", "")


def changes_to_data(
    changes: CHANGES,
    include_last_updated_at: T.Optional[bool] = True,
    only_include_changed_values: T.Optional[bool] = True,
) -> dict[str, str]:
    LAST_UPDATED_AT_STR = "last_updated_at"
    MAX_STR_LEN = 300

    def to_strikethrough(b: T.Any, a: T.Any) -> str:
        before_str = pretty_str(b)[0:MAX_STR_LEN]
        after_str = pretty_str(a)[0:MAX_STR_LEN]
        return f"~`{before_str}`~\n`{after_str}`"

    data = {}
    for field_name, (before, after) in changes.items():
        if only_include_changed_values:
            if before == after:
                continue
        if field_name == LAST_UPDATED_AT_STR:
            continue
        data[field_name] = to_strikethrough(b=before, a=after)
    if include_last_updated_at:
        if b_and_a := changes.get(LAST_UPDATED_AT_STR):
            (before, after) = b_and_a
            data[LAST_UPDATED_AT_STR] = to_strikethrough(b=before, a=after)
    return data


def make_possessive(name: str) -> str:
    if name.endswith("s"):
        return name + "'"
    else:
        return name + "'s"
