from typing import Any, List, Optional, Union

import sqlalchemy
from sqlalchemy.sql.type_api import TypeEngine
from strong_typing.schema import JsonType

from ..api import DAPClientError
from ..dap_types import VersionedSchema

SqlAlchemyType = Union[
    sqlalchemy.BigInteger,
    sqlalchemy.Integer,
    sqlalchemy.SmallInteger,
    sqlalchemy.Float,
    sqlalchemy.Double,
    sqlalchemy.Enum,
    sqlalchemy.TIMESTAMP,
    sqlalchemy.String,
    sqlalchemy.JSON,
    sqlalchemy.Boolean,
    sqlalchemy.ARRAY,
]


def match_type(
    schema: JsonType, namespace: str, table_name: str, prop_name: str
) -> TypeEngine[Any]:
    detected_type: Optional[SqlAlchemyType] = None

    if "oneOf" in schema:
        for oneOfTypes in schema["oneOf"]:
            if oneOfTypes["type"] != "string":
                raise OneOfTypeSchemaError(table_name)

        return sqlalchemy.String()

    if "type" not in schema:
        raise NoTypeSpecifiedError(table_name, prop_name)

    type_name = schema["type"]

    if type_name == "integer":
        if schema["format"] == "int64":
            detected_type = sqlalchemy.BigInteger()
        elif schema["format"] == "int32":
            detected_type = sqlalchemy.Integer()
        elif schema["format"] == "int16":
            detected_type = sqlalchemy.SmallInteger()

    elif type_name == "number":
        if "format" not in schema:
            detected_type = sqlalchemy.Float()

        elif schema["format"] == "float64":
            detected_type = sqlalchemy.Double()

    elif type_name == "string":
        if "enum" in schema:
            enum_name = f"{table_name}__{prop_name}"
            detected_type = sqlalchemy.Enum(
                *schema["enum"], name=enum_name, create_type=True, schema=namespace
            )

        elif "format" in schema and schema["format"] == "date-time":
            detected_type = sqlalchemy.TIMESTAMP(timezone=False)

        elif "maxLength" in schema:
            detected_type = sqlalchemy.String(length=schema["maxLength"])
        else:
            detected_type = sqlalchemy.String()

    elif type_name == "object":
        detected_type = sqlalchemy.JSON()

    elif type_name == "boolean":
        detected_type = sqlalchemy.Boolean()

    elif type_name == "array":
        if "items" not in schema:
            raise NoArrayItemTypeSpecifiedError(table_name, prop_name)

        items_schema = schema["items"]
        detected_type = sqlalchemy.ARRAY(
            match_type(items_schema, namespace, table_name, prop_name)
        )

    if detected_type is None:
        raise UnrecognizedTypeError(table_name, prop_name)

    return detected_type


def get_comment(schema: JsonType) -> str:
    comm = schema["description"] if "description" in schema else ""
    if type(comm) != str:
        raise NoStringDescriptionError

    return comm


class DAPSchemaParsingError(DAPClientError):
    pass


class NoStringDescriptionError(DAPSchemaParsingError):
    def __init__(self) -> None:
        super().__init__("`description` of property in schema must be a string")


class UnrecognizedTypeError(DAPSchemaParsingError):
    def __init__(self, table_name: str, prop_name: str) -> None:
        super().__init__(f"Cannot find Column type for {table_name}.{prop_name}")


class NoArrayItemTypeSpecifiedError(DAPSchemaParsingError):
    def __init__(self, table_name: str, prop_name: str) -> None:
        super().__init__(
            f"No item type is specified for array type in {table_name}.{prop_name}"
        )


class NoTypeSpecifiedError(DAPSchemaParsingError):
    def __init__(self, table_name: str, prop_name: str) -> None:
        super().__init__(
            f"Cannot recognize type without `type` field in {table_name}.{prop_name}"
        )


class CompositeKeyError(DAPSchemaParsingError):
    "Raised when the table schema has a composite primary key that comprises of multiple fields/columns."

    def __init__(self, table_name: str) -> None:
        super().__init__(f"Composite keys are not supported. Found in {table_name}")


class OneOfTypeSchemaError(DAPSchemaParsingError):
    def __init__(self, table_name: str) -> None:
        super().__init__(f"Only string is supported for oneOf types: {table_name}")


def create_table_definition(
    namespace: str, table_name: str, versioned_schema: VersionedSchema
) -> sqlalchemy.Table:
    """
    Creates SQLAlchemy table definition with the least step.

    :param namespace: Namespace that table belongs to.
    :param table_name: Identifier of the table.
    :param versioned_schema: Schema that the table conforms to.
    :returns: Table definition.
    :raises CompositeKeyError: The table has a composite primary key.
    """

    schema = versioned_schema.schema["properties"]
    key_schema = schema["key"]
    key_schema_props = key_schema["properties"]

    if len(key_schema_props) != 1:
        raise CompositeKeyError(table_name)

    value_schema = schema["value"]
    value_schema_props = value_schema["properties"]
    columns: List[sqlalchemy.Column] = []

    required_keys = key_schema.get("required", [])
    for id_prop_name in key_schema_props:
        id_schema = key_schema_props[id_prop_name]

        column_type = match_type(id_schema, namespace, table_name, id_prop_name)

        columns.append(
            sqlalchemy.Column(
                id_prop_name,
                column_type,
                primary_key=True,
                nullable=(id_prop_name not in required_keys),
                comment=get_comment(id_schema),
            )
        )

    required_values = value_schema.get("required", [])
    for prop_name in value_schema_props:
        prop_schema = value_schema_props[prop_name]
        column_type = match_type(prop_schema, namespace, table_name, prop_name)

        columns.append(
            sqlalchemy.Column(
                prop_name,
                column_type,
                nullable=(prop_name not in required_values),
                comment=get_comment(prop_schema),
            )
        )

    # create table model
    metadata = sqlalchemy.MetaData(schema=namespace)
    return sqlalchemy.Table(table_name, metadata, *columns)
