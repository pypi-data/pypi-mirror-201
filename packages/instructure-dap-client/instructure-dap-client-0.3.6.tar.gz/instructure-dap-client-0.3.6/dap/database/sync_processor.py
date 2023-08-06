from types import TracebackType
from typing import Optional, Type

from sqlalchemy import Connection, Inspector, Table, inspect

from ..dap_types import VersionedSchema
from ..model.metadata import create_table_definition
from ..type_conversion import (
    ConverterDict,
    JsonRecord,
    create_delete_converters,
    create_upsert_converters,
)
from .base_processor import BaseBatch, BaseSyncProcessor, ContextAwareObject
from .connection import DatabaseSession
from .database_errors import NonExistingTableError
from .database_operations import DatabaseDelete, DatabaseUpsert


def _check_table(db_conn: Connection, table_def: Table) -> None:
    inspector: Inspector = inspect(db_conn)
    if not inspector.has_table(table_def.name, table_def.schema):
        raise NonExistingTableError(table_def.schema or "", table_def.name)


class SyncProcessor(BaseSyncProcessor):
    """
    Inserts/updates/deletes records acquired from the DAP service into/in/from a database table.

    Processes synchronization records that can be either UPSERT or DELETE.
    As preparation, it checks if target table exists.
    """

    _db_connection: DatabaseSession
    _table_def: Table
    _upsert_converters: ConverterDict
    _delete_converters: ConverterDict

    def __init__(
        self,
        db_connection: DatabaseSession,
        namespace: str,
        table_name: str,
        schema: VersionedSchema,
    ) -> None:
        self._db_connection = db_connection
        self._table_def = create_table_definition(namespace, table_name, schema)

        self._upsert_converters = create_upsert_converters(self._table_def)
        self._delete_converters = create_delete_converters(self._table_def)

    async def prepare(self) -> None:
        async with self._db_connection.context() as conn:
            await conn.run_sync(lambda c: _check_table(c, self._table_def))

    def batch(self, obj: ContextAwareObject) -> BaseBatch:
        return SyncBatch(
            DatabaseUpsert(self._db_connection, self._table_def, obj),
            self._upsert_converters,
            DatabaseDelete(self._db_connection, self._table_def, obj),
            self._delete_converters,
        )

    async def close(self) -> None:
        pass


class SyncBatch(BaseBatch):
    _db_upsert_op: DatabaseUpsert
    _upsert_converters: ConverterDict

    _db_delete_op: DatabaseDelete
    _delete_converters: ConverterDict

    def __init__(
        self,
        upsert_op: DatabaseUpsert,
        upsert_converters: ConverterDict,
        delete_op: DatabaseDelete,
        delete_converters: ConverterDict,
    ) -> None:
        self._db_upsert_op = upsert_op
        self._upsert_converters = upsert_converters
        self._db_delete_op = delete_op
        self._delete_converters = delete_converters

    async def process(self, record: JsonRecord) -> None:
        if "value" in record:
            sql_item = {
                col_name: converter(record)
                for col_name, converter in self._upsert_converters.items()
            }
            await self._db_upsert_op.process(sql_item)
        else:
            sql_item = {
                col_name: converter(record)
                for col_name, converter in self._delete_converters.items()
            }
            await self._db_delete_op.process(sql_item)

    async def __aenter__(self) -> "BaseBatch":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._db_upsert_op.flush()
        await self._db_delete_op.flush()
