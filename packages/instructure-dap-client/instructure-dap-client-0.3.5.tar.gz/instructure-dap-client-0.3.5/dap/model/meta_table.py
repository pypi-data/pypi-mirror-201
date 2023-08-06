import json
from datetime import datetime, timezone

import sqlalchemy
from sqlalchemy import bindparam, Connection, Inspector, inspect
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.ddl import CreateSchema
from strong_typing.core import JsonType, Schema
from strong_typing.serialization import json_to_object, json_dump_string

from ..dap_types import VersionedSchema, GetTableDataResult
from ..processing_error import SchemaVersionMismatchError


def _create_metatable_def(namespace: str) -> sqlalchemy.Table:
    metadata = sqlalchemy.MetaData(schema=namespace)
    metatable = sqlalchemy.Table(
        "dap_meta",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("namespace", sqlalchemy.String(64), nullable=False),
        sqlalchemy.Column("source_table", sqlalchemy.String(64), nullable=False),
        sqlalchemy.Column("timestamp", sqlalchemy.DateTime(), nullable=False),
        sqlalchemy.Column("schema_version", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("target_schema", sqlalchemy.String(64), nullable=True),
        sqlalchemy.Column("target_table", sqlalchemy.String(64), nullable=False),
        sqlalchemy.Column(
            "schema_description_format", sqlalchemy.String(64), nullable=False
        ),
        sqlalchemy.Column("schema_description", sqlalchemy.Text(), nullable=False),
        sqlalchemy.UniqueConstraint(
            "namespace",
            "source_table",
            name="UQ__dap_meta__namespace__source_table",
        ),
    )
    return metatable


class _MetatableRecord:
    namespace: str
    table_name: str
    timestamp: datetime
    versioned_schema: VersionedSchema
    metadata: sqlalchemy.MetaData

    @staticmethod
    async def load(
        namespace: str,
        table_name: str,
        db_conn: AsyncConnection,
        metatable_def: sqlalchemy.Table,
    ) -> "_MetatableRecord":
        result = await db_conn.execute(
            metatable_def.select()
            .where(metatable_def.c.namespace == namespace)
            .where(metatable_def.c.source_table == table_name)
        )
        metatable_record = result.first()
        if metatable_record is None:
            raise NoMetadataError(namespace, table_name)

        schema_description_format: str = metatable_record._mapping[
            "schema_description_format"
        ]
        if schema_description_format != "json":
            raise WrongSchemaDescriptionError(schema_description_format)

        schema_description: JsonType = json.loads(
            metatable_record._mapping["schema_description"]
        )

        schema_version: int = metatable_record._mapping["schema_version"]
        versioned_schema: VersionedSchema = VersionedSchema(
            json_to_object(Schema, schema_description), schema_version
        )

        record = _MetatableRecord(
            namespace, table_name, versioned_schema, metatable_def.metadata
        )
        record.timestamp = metatable_record._mapping["timestamp"]
        return record

    def __init__(
        self,
        namespace: str,
        table_name: str,
        versioned_schema: VersionedSchema,
        metadata: sqlalchemy.MetaData,
    ) -> None:
        self.namespace = namespace
        self.table_name = table_name
        self.versioned_schema = versioned_schema
        self.metadata = metadata


class MetatableManager:
    _db_connection: AsyncConnection
    _namespace: str
    _table_name: str
    _metatable_def: sqlalchemy.Table

    def __init__(
        self, db_connection: AsyncConnection, namespace: str, table_name: str
    ) -> None:
        self._db_connection = db_connection
        self._namespace = namespace
        self._table_name = table_name
        self._metatable_def = _create_metatable_def(namespace)

    async def last_sync_datetime(self) -> datetime:
        """
        :returns: datetime of last updates on table
        """
        metatable_record = await _MetatableRecord.load(
            self._namespace, self._table_name, self._db_connection, self._metatable_def
        )
        return metatable_record.timestamp.replace(tzinfo=timezone.utc)

    async def initialize(
        self, table_schema: VersionedSchema, table_data: GetTableDataResult
    ) -> None:
        """
        Creates table in database schema and records an entry in it.
        """
        await self._db_connection.run_sync(lambda c: self._create_tables(c))
        await self._db_connection.execute(
            self._metatable_def.insert(),
            [
                {
                    "namespace": self._namespace,
                    "source_table": self._table_name,
                    "timestamp": table_data.timestamp.astimezone(
                        tz=timezone.utc
                    ).replace(tzinfo=None),
                    "schema_version": table_data.schema_version,
                    "target_schema": self._namespace,
                    "target_table": self._table_name,
                    "schema_description_format": "json",
                    "schema_description": json_dump_string(table_schema.schema),
                }
            ],
        )

    async def synchronize(self, table_data: GetTableDataResult) -> None:
        """
        Updates related record of meta table with recent table data.
        """
        await self._check_sync(table_data)
        await self._db_connection.execute(
            (
                self._metatable_def.update()
                .where(self._metatable_def.c.namespace == self._namespace)
                .where(self._metatable_def.c.source_table == self._table_name)
                .values(timestamp=bindparam("new_timestamp"))
            ),
            [
                {
                    "new_timestamp": table_data.timestamp.astimezone(
                        timezone.utc
                    ).replace(tzinfo=None)
                }
            ],
        )

    async def _check_sync(self, table_data: GetTableDataResult) -> None:
        metatable_record = await _MetatableRecord.load(
            self._namespace, self._table_name, self._db_connection, self._metatable_def
        )

        if metatable_record.versioned_schema.version != table_data.schema_version:
            raise SchemaVersionMismatchError(
                table_data.schema_version, metatable_record.versioned_schema.version
            )

    async def drop(self) -> None:
        await self._db_connection.execute(
            self._metatable_def.delete()
            .where(self._metatable_def.c.namespace == self._namespace)
            .where(self._metatable_def.c.source_table == self._table_name)
        )

    def _create_tables(self, db_conn: Connection) -> None:
        inspector: Inspector = inspect(db_conn)
        if self._metatable_def.schema is not None and not inspector.has_schema(
            self._metatable_def.schema
        ):
            db_conn.execute(CreateSchema(self._metatable_def.schema))  # type: ignore

        self._metatable_def.metadata.create_all(db_conn)


class MetadataError(Exception):
    """
    Generic base class for specific meta-table related errors.
    """


class NoMetadataError(MetadataError):
    def __init__(self, namespace: str, table_name: str) -> None:
        super().__init__(
            f"metadata not found for table `{table_name}` in `{namespace}`"
        )


class WrongSchemaDescriptionError(MetadataError):
    def __init__(self, schema_description_format: str) -> None:
        super().__init__(
            f"wrong schema description format; expected: json, got: {schema_description_format}"
        )
