from typing import Tuple

from sqlalchemy import Connection, Inspector, Table, inspect
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.ddl import CreateSchema

from ..dap_types import VersionedSchema
from ..database.db_operations import DBOperations
from ..model.metadata import create_table_definition
from ..type_conversion import JsonRecord, create_copy_converters
from .base_processor import BaseInitProcessor, ContextAwareObject
from .database_errors import TableAlreadyExistsError


def _create_tables(db_conn: Connection, table_def: Table) -> None:
    inspector: Inspector = inspect(db_conn)

    if inspector.has_table(table_def.name, table_def.schema):
        raise TableAlreadyExistsError(table_def.name, table_def.schema)

    if table_def.schema is not None and not inspector.has_schema(table_def.schema):
        db_conn.execute(CreateSchema(table_def.schema))  # type: ignore

    table_def.metadata.create_all(db_conn)


class InitProcessor(BaseInitProcessor):
    """
    Handles processing of data entries during initialization.
    In `prepare` it creates table specified by `namespace` and `table_name`.
    Then it passes JSON records towards `DBOperations.copy`.
    Finally, it makes `DBOperations` flush it's content in `close` method.
    """

    _db_connection: AsyncConnection
    _table_def: Table
    _db_operations: DBOperations
    _converters: Tuple

    def __init__(
        self,
        db_connection: AsyncConnection,
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        self._db_connection = db_connection
        self._table_def = create_table_definition(namespace, table_name, table_schema)
        self._db_operations = DBOperations(db_connection, self._table_def)
        self._converters = create_copy_converters(self._table_def)

    async def prepare(self) -> None:
        await self._db_connection.run_sync(lambda c: _create_tables(c, self._table_def))

    async def process(self, record: JsonRecord, obj: ContextAwareObject) -> None:
        await self._db_operations.copy(
            tuple(converter(record) for converter in self._converters), obj
        )

    async def close(self) -> None:
        await self._db_operations.flush()
