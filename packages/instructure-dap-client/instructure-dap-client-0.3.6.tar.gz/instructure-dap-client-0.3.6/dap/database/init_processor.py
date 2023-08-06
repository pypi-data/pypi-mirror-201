from types import TracebackType
from typing import Optional, Tuple, Type

from sqlalchemy import Connection, Inspector, Table, inspect
from sqlalchemy.sql.ddl import CreateSchema

from ..dap_types import VersionedSchema
from ..model.metadata import create_table_definition
from ..type_conversion import JsonRecord, create_copy_converters
from .base_processor import BaseBatch, BaseInitProcessor, ContextAwareObject
from .connection import DatabaseSession
from .database_errors import TableAlreadyExistsError
from .database_operations import DatabaseCopy


def _create_tables(db_conn: Connection, table_def: Table) -> None:
    inspector: Inspector = inspect(db_conn)

    if inspector.has_table(table_def.name, table_def.schema):
        raise TableAlreadyExistsError(table_def.name, table_def.schema)

    if table_def.schema is not None and not inspector.has_schema(table_def.schema):
        db_conn.execute(CreateSchema(table_def.schema))  # type: ignore

    table_def.metadata.create_all(db_conn)


class InitProcessor(BaseInitProcessor):
    """
    Creates and populates an empty database table with records acquired from the DAP service.
    """

    _db_connection: DatabaseSession
    _table_def: Table
    _converters: Tuple

    def __init__(
        self,
        db_connection: DatabaseSession,
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        self._db_connection = db_connection
        self._table_def = create_table_definition(namespace, table_name, table_schema)
        self._converters = create_copy_converters(self._table_def)

    async def prepare(self) -> None:
        async with self._db_connection.context() as conn:
            await conn.run_sync(lambda c: _create_tables(c, self._table_def))

    def batch(self, obj: ContextAwareObject) -> BaseBatch:
        return InitBatch(
            DatabaseCopy(self._db_connection, self._table_def, obj), self._converters
        )

    async def close(self) -> None:
        pass


class InitBatch(BaseBatch):
    _db_copy_op: DatabaseCopy
    _converters: Tuple

    def __init__(self, copy_op: DatabaseCopy, converters: Tuple) -> None:
        self._db_copy_op = copy_op
        self._converters = converters

    async def process(self, record: JsonRecord) -> None:
        await self._db_copy_op.process(
            tuple(converter(record) for converter in self._converters)
        )

    async def __aenter__(self) -> "BaseBatch":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._db_copy_op.flush()
