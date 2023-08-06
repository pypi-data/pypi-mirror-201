from typing import TYPE_CHECKING, Any, Tuple, TypeVar, Union, overload

import attrs

from cleanchausie.consts import empty
from cleanchausie.errors import Error, Errors, ValidationError

if TYPE_CHECKING:
    from cleanchausie.fields.field import Field
    from cleanchausie.fields.validation import Value

T = TypeVar("T")


def noop(value: T) -> T:
    return value


@overload
def wrap_result(field: Tuple[Union[str, int], ...], result: Error) -> Error:
    ...


@overload
def wrap_result(
    field: Tuple[Union[str, int], ...], result: "Value"
) -> "Value":
    ...


def wrap_result(
    field: Tuple[Union[str, int], ...], result: Any
) -> Union["Value", Error]:
    from cleanchausie.fields.validation import Value

    if isinstance(result, Error):
        return attrs.evolve(result, field=field + result.field)
    elif not isinstance(result, Value):
        return Value(value=result)
    return result


def clean_field(
    field: "Field[T]", data: Any, context: Any = empty
) -> Union[T, ValidationError]:
    """Validate data using a specific field.

    This can be helpful for defining reusable fields, or for using complex
    fields as top-level schemas as well.
    """
    from cleanchausie.fields.validation import validate_field

    result = validate_field(
        field=field,
        path=(),
        root_value=data,
        value=data,
        context=context,
        intermediate_results={},
    )
    if isinstance(result, Errors):
        return ValidationError(result.flatten())
    return result.value


def serialize_field(field: "Field[T]", value: T) -> Any:
    """Serialize a value using a specific field.

    It's assumed that the value has already been validated.
    """
    return field.serialize_func(value)
