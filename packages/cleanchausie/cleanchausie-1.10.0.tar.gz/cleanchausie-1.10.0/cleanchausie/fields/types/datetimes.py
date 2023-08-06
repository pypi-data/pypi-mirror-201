import datetime
from typing import Union

from dateutil import parser

from cleanchausie.errors import Error
from cleanchausie.fields.field import Field, field

from .strings import StrField


def TimeDeltaField() -> Field[datetime.timedelta]:  # noqa: N802
    @field
    def _timedelta_field(
        value: Union[int, datetime.timedelta]
    ) -> datetime.timedelta:
        # value is either already a timedelta or is an int in seconds
        if isinstance(value, datetime.timedelta):
            return value
        elif isinstance(value, int):
            return datetime.timedelta(seconds=value)
        else:
            raise TypeError(f"Unhandled type '{type(value)}'")

    return _timedelta_field


def DateTimeField() -> Field[datetime.datetime]:  # noqa: N802
    def _serialize(value: datetime.datetime) -> str:
        return value.isoformat()

    @field(parents=(StrField(),), serialize_func=_serialize)
    def _datetimefield(value: str) -> Union[Error, datetime.datetime]:
        # TODO should this reject naive datetimes? or assume a timezone?
        try:
            # TODO should we use ciso8601 to parse? It's a bit stricter, but much faster.
            return parser.parse(value)
        except ValueError:
            return Error(msg=f"Could not parse datetime from '{value}'.")

    return _datetimefield
