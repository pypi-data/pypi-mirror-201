import asyncio
import logging
from time import time
from typing import Any, Dict, List, Optional, Tuple

import asyncpg
from sqlalchemy import Delete, Table, bindparam
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.dml import Insert

from ..database.base_processor import ContextAwareObject
from .database_errors import DatabaseConnectionError

RECORDS_PER_FLUSH = 1000000


class _RecordSet:
    object: ContextAwareObject
    records_to_copy: List[Tuple]
    records_to_upsert: List[Dict[str, Any]]
    records_to_delete: List[Dict[str, Any]]

    def __init__(self, obj: ContextAwareObject) -> None:
        self.object = obj
        self.records_to_copy = []
        self.records_to_upsert = []
        self.records_to_delete = []


class DBOperations:
    _db_conn: AsyncConnection
    _table_def: Table
    _db_lock: asyncio.Lock
    _recordsets_per_object: Dict[str, _RecordSet]
    _record_counter: int

    def __init__(self, db_conn: AsyncConnection, table_def: Table) -> None:
        self._db_conn = db_conn
        self._table_def = table_def
        self._db_lock = asyncio.Lock()
        self._recordsets_per_object = {}
        self._record_counter = 0

    async def copy(self, record: Tuple, obj: ContextAwareObject) -> None:
        recordset: _RecordSet = self._get_recordset(obj)
        recordset.records_to_copy.append(record)
        self._record_counter += 1
        if self._record_counter % RECORDS_PER_FLUSH == 0:
            await self.flush()

    async def upsert(self, record: Dict[str, Any], obj: ContextAwareObject) -> None:
        recordset: _RecordSet = self._get_recordset(obj)
        recordset.records_to_upsert.append(record)
        self._record_counter += 1
        if self._record_counter % RECORDS_PER_FLUSH == 0:
            await self.flush()

    async def delete(self, record: Dict[str, Any], obj: ContextAwareObject) -> None:
        recordset: _RecordSet = self._get_recordset(obj)
        recordset.records_to_delete.append(record)
        self._record_counter += 1
        if self._record_counter % RECORDS_PER_FLUSH == 0:
            await self.flush()

    async def flush(self) -> None:
        recordsets: List[_RecordSet] = list(self._recordsets_per_object.values())
        self._recordsets_per_object = {}
        self._record_counter = 0

        for recordset in recordsets:
            await self._flush_copies(recordset)
            await self._flush_upserts(recordset)
            await self._flush_deletions(recordset)

    async def _flush_copies(self, recordset: _RecordSet) -> None:
        if not recordset.records_to_copy:
            return

        sync_conn = self._db_conn.sync_connection
        if sync_conn is None:
            raise DatabaseConnectionError

        driver_conn: asyncpg.connection.Connection = (
            sync_conn.connection.driver_connection
        )
        if driver_conn is None:
            raise DatabaseConnectionError

        async with self._db_lock:
            logging.debug(
                f"Inserting {len(recordset.records_to_copy)} records from {recordset.object}"
            )
            start_time = time()
            await driver_conn.copy_records_to_table(
                schema_name=self._table_def.metadata.schema,
                table_name=self._table_def.name,
                columns=[col.name for col in self._table_def.columns],
                records=recordset.records_to_copy,
            )
            elapsed_time_ms = (time() - start_time) * 1000
            logging.info(
                f"Inserted {len(recordset.records_to_copy)} records from {recordset.object}"
            )
            logging.debug(f"Total elapsed time: {elapsed_time_ms} ms")
            logging.debug(
                f"Avg elapsed time per record: {elapsed_time_ms / len(recordset.records_to_copy)}"
            )

    async def _flush_deletions(self, recordset: _RecordSet) -> None:
        if not recordset.records_to_delete:
            return

        delete_statement: Delete = self._table_def.delete()
        for col in self._table_def.primary_key:
            delete_statement = delete_statement.where(
                self._table_def.c[col.name] == bindparam(col.name)
            )

        async with self._db_lock:
            logging.debug(
                f"Deleting {len(recordset.records_to_delete)} records from {recordset.object}"
            )
            start_time = time()
            await self._db_conn.execute(
                statement=delete_statement,
                parameters=recordset.records_to_delete,
            )
            elapsed_time_ms = (time() - start_time) * 1000
            logging.info(
                f"Deleted {len(recordset.records_to_delete)} records from {recordset.object}"
            )
            logging.debug(f"Total elapsed time: {elapsed_time_ms} ms")
            logging.debug(
                f"Avg elapsed time per record: {elapsed_time_ms / len(recordset.records_to_delete)}"
            )

    async def _flush_upserts(self, recordset: _RecordSet) -> None:
        if not recordset.records_to_upsert:
            return

        upsert_statement: Insert = insert(self._table_def).on_conflict_do_update(  # type: ignore
            constraint=self._table_def.primary_key, set_=self._table_def.c
        )

        async with self._db_lock:
            logging.debug(
                f"Upserting {len(recordset.records_to_upsert)} records from {recordset.object}"
            )
            start_time = time()
            await self._db_conn.execute(
                statement=upsert_statement,
                parameters=recordset.records_to_upsert,
            )
            elapsed_time_ms = (time() - start_time) * 1000
            logging.info(
                f"Upserted {len(recordset.records_to_upsert)} records from {recordset.object}"
            )
            logging.debug(f"Total elapsed time: {elapsed_time_ms} ms")
            logging.debug(
                f"Avg elapsed time per record: {elapsed_time_ms / len(recordset.records_to_upsert)}"
            )

    def _get_recordset(self, obj: ContextAwareObject) -> _RecordSet:
        recordset: Optional[_RecordSet] = self._recordsets_per_object.get(obj.id)
        if recordset is None:
            recordset = _RecordSet(obj)
            self._recordsets_per_object[obj.id] = recordset
        return recordset
