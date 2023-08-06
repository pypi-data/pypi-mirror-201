from typing import Any, Type, TypeVar, Union

from cleanchausie.errors import Error
from cleanchausie.fields.field import Field, field

T = TypeVar("T")


def InstanceField(of_type: Type[T]) -> Field[T]:  # noqa: N802
    @field
    def _instance_field(value: Any) -> Union[T, Error]:
        if isinstance(value, of_type):
            return value
        return Error(f"Expected an object of type {of_type.__name__}")

    return _instance_field
