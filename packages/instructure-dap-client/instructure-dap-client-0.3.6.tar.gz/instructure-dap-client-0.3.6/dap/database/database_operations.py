from typing import Any, Dict, Generic, List, Tuple, TypeVar

import asyncpg
from sqlalchemy import Delete, Table, bindparam
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.dml import Insert

from ..timer import Timer
from .base_processor import ContextAwareObject
from .connection import DatabaseSession
from .database_errors import DatabaseConnectionError

RECORDS_PER_FLUSH = 1000000

T = TypeVar("T")


class DatabaseOperation(Generic[T]):
    _connection: DatabaseSession
    _table_def: Table
    _context: ContextAwareObject
    _records: List[T]
    _record_counter: int

    def __init__(
        self,
        connection: DatabaseSession,
        table_def: Table,
        context: ContextAwareObject,
    ) -> None:
        self._connection = connection
        self._table_def = table_def
        self._context = context
        self._records = []
        self._record_counter = 0

    async def process(self, record: T) -> None:
        self._records.append(record)
        self._record_counter += 1
        if self._record_counter % RECORDS_PER_FLUSH == 0:
            await self.flush()

    async def flush(self) -> None:
        if not self._records:
            return
        await self._execute()
        self._records = []

    async def _execute(self) -> None:
        pass


class DatabaseCopy(DatabaseOperation[Tuple]):
    async def _execute(self) -> None:
        async with Timer(
            f"inserting {len(self._records)} records from {self._context}"
        ):
            async with self._connection.context() as conn:
                raw_conn = await conn.get_raw_connection()

                driver_conn: asyncpg.Connection = raw_conn.driver_connection
                if driver_conn is None:
                    raise DatabaseConnectionError

                await driver_conn.copy_records_to_table(
                    schema_name=self._table_def.metadata.schema,
                    table_name=self._table_def.name,
                    columns=[col.name for col in self._table_def.columns],
                    records=self._records,
                )


class DatabaseUpsert(DatabaseOperation[Dict[str, Any]]):
    async def _execute(self) -> None:
        if not self._records:
            return

        upsert_statement: Insert = insert(self._table_def).on_conflict_do_update(  # type: ignore
            constraint=self._table_def.primary_key, set_=self._table_def.c
        )

        async with Timer(
            f"upserting {len(self._records)} records from {self._context}"
        ):
            async with self._connection.context() as conn:
                await conn.execute(
                    statement=upsert_statement,
                    parameters=self._records,
                )


class DatabaseDelete(DatabaseOperation[Dict[str, Any]]):
    async def _execute(self) -> None:
        delete_statement: Delete = self._table_def.delete()
        for col in self._table_def.primary_key:
            delete_statement = delete_statement.where(
                self._table_def.c[col.name] == bindparam(col.name)
            )

        async with Timer(f"deleting {len(self._records)} records from {self._context}"):
            async with self._connection.context() as conn:
                await conn.execute(
                    statement=delete_statement,
                    parameters=self._records,
                )
