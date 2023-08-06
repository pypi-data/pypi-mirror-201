from inspect import isclass
from typing import Any, Dict, Type, TypeVar, Union, overload

from cleanchausie import ValidationError
from cleanchausie.consts import empty
from cleanchausie.schema import Schema
from cleanchausie.schema_definition import (
    SchemaDefinition,
    clean_def,
    serialize_def,
)

T = TypeVar("T")

T_SCHEMA = TypeVar("T_SCHEMA", bound=Schema)


@overload
def clean(
    schema_or_def: Type[T_SCHEMA],
    data: Any,
    context: Any = empty,
) -> Union[T_SCHEMA, ValidationError]:
    ...


@overload
def clean(
    schema_or_def: SchemaDefinition[T],
    data: Any,
    context: Any = empty,
) -> Union[T, ValidationError]:
    ...


def clean(
    schema_or_def: Union[Type[T_SCHEMA], SchemaDefinition[T]],
    data: Any,
    context: Any = empty,
) -> Any:
    if isclass(schema_or_def) and issubclass(schema_or_def, Schema):
        return clean_def(schema_or_def._schema_definition, data, context)
    elif isinstance(schema_or_def, SchemaDefinition):
        return clean_def(schema_or_def, data, context)
    else:
        raise TypeError(f"Cannot clean type: {type(schema_or_def).__name__}")


@overload
def serialize(schema_or_def: Schema, data: Any = empty) -> Dict:
    ...


@overload
def serialize(schema_or_def: Type[Schema], data: Any) -> Dict:
    ...


@overload
def serialize(schema_or_def: SchemaDefinition, data: Any) -> Dict:
    ...


def serialize(
    schema_or_def: Union[Type[Schema], Schema, SchemaDefinition],
    data: Any = empty,
) -> Dict:
    if isclass(schema_or_def) and issubclass(schema_or_def, Schema):
        assert data is not empty
        return serialize_def(schema_or_def._schema_definition, data)
    if isinstance(schema_or_def, Schema):
        assert data is empty
        return serialize_def(schema_or_def._schema_definition, schema_or_def)
    elif isinstance(schema_or_def, SchemaDefinition):
        assert data is not empty
        return serialize_def(schema_or_def, data)
    else:
        raise TypeError(
            f"Cannot serialize type: {type(schema_or_def).__name__}"
        )
