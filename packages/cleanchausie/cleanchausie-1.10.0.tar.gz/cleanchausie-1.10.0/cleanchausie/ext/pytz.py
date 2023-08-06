from typing import Optional, Union

import pytz
from pytz import BaseTzInfo

from cleanchausie.errors import Error
from cleanchausie.fields.field import Field, field


def PytzTimezoneField() -> Field[BaseTzInfo]:  # noqa: N802
    def _serialize_fn(value: BaseTzInfo) -> Optional[str]:
        return value.tzname(None)

    @field(serialize_func=_serialize_fn)
    def _pytz_timezone_field(value: str) -> Union[BaseTzInfo, Error]:
        try:
            return pytz.timezone(value)
        except pytz.UnknownTimeZoneError:
            return Error(msg=f"Unknown timezone: {value}")

    return _pytz_timezone_field
