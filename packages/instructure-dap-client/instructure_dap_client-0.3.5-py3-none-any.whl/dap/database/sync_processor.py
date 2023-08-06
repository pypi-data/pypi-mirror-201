import logging

from sqlalchemy import Connection, Inspector, Table, inspect
from sqlalchemy.ext.asyncio import AsyncConnection

from ..dap_types import VersionedSchema
from ..database.db_operations import DBOperations
from ..model.metadata import create_table_definition
from ..type_conversion import (
    ConverterDict,
    JsonRecord,
    create_delete_converters,
    create_upsert_converters,
)
from .base_processor import BaseSyncProcessor, ContextAwareObject
from .database_errors import NonExistingTableError


def _check_table(db_conn: Connection, table_def: Table) -> None:
    inspector: Inspector = inspect(db_conn)
    if not inspector.has_table(table_def.name, table_def.schema):
        raise NonExistingTableError(table_def.schema or "", table_def.name)


class SyncProcessor(BaseSyncProcessor):
    """
    Processes synchronization records that can be either UPSERT or DELETE.
    As preparation, it checks if target table exists.
    Method `process` just passes entries towards `DBOperations` according to the type of record.
    Finally, it makes `DBOperations` flush it's content in `close` method.
    """

    _db_connection: AsyncConnection
    _table_def: Table
    _db_operations: DBOperations
    _change_count: int
    _upsert_converters: ConverterDict
    _delete_converters: ConverterDict

    def __init__(
        self,
        db_connection: AsyncConnection,
        namespace: str,
        table_name: str,
        schema: VersionedSchema,
    ) -> None:
        self._db_connection = db_connection
        self._table_def = create_table_definition(namespace, table_name, schema)
        self._db_operations = DBOperations(db_connection, self._table_def)
        self._change_count = 0

        self._upsert_converters = create_upsert_converters(self._table_def)
        self._delete_converters = create_delete_converters(self._table_def)

    async def prepare(self) -> None:
        await self._db_connection.run_sync(lambda c: _check_table(c, self._table_def))

    async def process_upsert(self, record: JsonRecord, obj: ContextAwareObject) -> None:
        sql_item = {
            col_name: converter(record)
            for col_name, converter in self._upsert_converters.items()
        }

        await self._db_operations.upsert(sql_item, obj)
        self._change_count += 1

    async def process_delete(self, record: JsonRecord, obj: ContextAwareObject) -> None:
        sql_item = {
            col_name: converter(record)
            for col_name, converter in self._delete_converters.items()
        }
        await self._db_operations.delete(sql_item, obj)
        self._change_count += 1

    async def close(self) -> None:
        if self._change_count == 0:
            logging.info(f"Nothing to sync")

        await self._db_operations.flush()
