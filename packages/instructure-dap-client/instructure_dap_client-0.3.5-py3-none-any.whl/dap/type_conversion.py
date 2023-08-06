import abc
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar

import aiohttp
from sqlalchemy import ARRAY, JSON, TIMESTAMP, BigInteger, Boolean, Column, Double
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, Integer, SmallInteger, String, Table
from strong_typing.core import JsonType
from strong_typing.serialization import json_dump_string

from .payload import get_json_lines_from_gzip_stream
from .timestamp import valid_naive_datetime

T = TypeVar("T")

JsonRecord = Dict[str, JsonType]


def _get_optional_value(
    column_name: str, type_cast: Callable[[JsonType], Any], record_json: JsonRecord
) -> Optional[Any]:
    "Extracts an optional value from a nullable column."

    value = record_json["value"].get(column_name)
    return type_cast(value) if value is not None else None


def _get_column_converter(col: Column) -> Callable[[JsonRecord], Any]:
    "Returns a lambda function that extracts a column value from the JSON representation of a record."

    column_type = type(col.type)

    type_cast: Callable[[JsonType], Any]
    if (
        column_type is Integer
        or column_type is SmallInteger
        or column_type is BigInteger
    ):
        type_cast = int
    elif column_type is Float or column_type is Double:
        type_cast = float
    elif column_type is String:
        type_cast = str
    elif column_type is SqlEnum:
        type_cast = _identity
    elif column_type is JSON:
        type_cast = json_dump_string
    elif column_type is TIMESTAMP:
        type_cast = valid_naive_datetime
    elif column_type is Boolean:
        type_cast = bool
    elif column_type is ARRAY:
        type_cast = _valid_list
    else:
        raise TypeError(f"cannot convert to {column_type}")

    column_name = col.name
    if col.primary_key:
        return lambda record_json: type_cast(record_json["key"][column_name])
    elif col.nullable:
        return lambda record_json: _get_optional_value(
            column_name, type_cast, record_json
        )
    else:
        return lambda record_json: type_cast(record_json["value"][column_name])


def _identity(obj: T) -> T:
    return obj


def _valid_list(obj: Any) -> list:
    if type(obj) is list:
        return obj
    else:
        raise TypeError(f"object is not a list: {obj}")


ConverterDict = Dict[str, Callable[[JsonRecord], Any]]


def create_upsert_converters(table_def: Table) -> ConverterDict:
    # create a tuple of converter objects for each column for UPSERT records
    return {col.name: _get_column_converter(col) for col in table_def.columns}


def create_delete_converters(table_def: Table) -> ConverterDict:
    # create a tuple of converter objects for each column for DELETE records
    return {col.name: _get_column_converter(col) for col in table_def.primary_key}


def create_copy_converters(table_def: Table) -> Tuple:
    return tuple(_get_column_converter(col) for col in table_def.columns)


class AbstractRecordVisitor(abc.ABC):
    "Base class for synchronization visitors that insert/update, or delete a record."

    @abc.abstractmethod
    async def upsert(self, record: JsonRecord) -> None:
        ...

    @abc.abstractmethod
    async def delete(self, record: JsonRecord) -> None:
        ...


async def process_resource_for_sync(
    stream: aiohttp.StreamReader, visitor: AbstractRecordVisitor
) -> None:
    "Reads JSON records from a stream and makes them upserted or deleted via the visitor."

    async for json_content in get_json_lines_from_gzip_stream(stream):
        if "value" in json_content:
            await visitor.upsert(json_content)
        else:
            await visitor.delete(json_content)
