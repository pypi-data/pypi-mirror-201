from typing import TypeVar, Union

from cleanchausie.consts import OMITTED


def getter(dict_or_obj, field_name, default):
    if isinstance(dict_or_obj, dict):
        return dict_or_obj.get(field_name, default)

    return getattr(dict_or_obj, field_name, default)


T = TypeVar("T")
D = TypeVar("D")


def fallback(value: Union[T, OMITTED], default: D) -> Union[T, D]:
    if isinstance(default, OMITTED):
        raise ValueError("The default cannot be OMITTED")

    if not isinstance(value, OMITTED):
        return value

    return default
