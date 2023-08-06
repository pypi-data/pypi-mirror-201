from typing import Optional

from ..api import DAPSession
from ..database.base_processor import BaseInitProcessor, BaseSyncProcessor
from ..database.connection import DatabaseSession
from ..database.init_processor import InitProcessor
from ..database.sync_processor import SyncProcessor
from ..downloader import IncrementalClientFactory, SnapshotClientFactory
from ..model.meta_table import MetaTableManager


class SQLReplicator:
    """
    Encapsulates logic that replicates changes acquired from DAP API in a SQL database.
    """

    def __init__(self, session: DAPSession, connection: DatabaseSession) -> None:
        self._session = session
        self._connection = connection

    async def initialize(
        self,
        namespace: str,
        table_name: str,
        processor: Optional[BaseInitProcessor] = None,
    ) -> None:
        """
        Initializes database table. Processor
        """
        client = await SnapshotClientFactory(
            self._session, namespace, table_name
        ).get_client()

        if processor is None:
            processor = InitProcessor(
                db_connection=self._connection,
                namespace=namespace,
                table_name=table_name,
                table_schema=client.table_schema,
            )

        await processor.prepare()

        await MetaTableManager(self._connection, namespace, table_name).initialize(
            table_schema=client.table_schema, table_data=client.table_data
        )

        await client.download(processor)

        async with self._connection.context() as conn:
            await conn.commit()

    async def synchronize(
        self,
        namespace: str,
        table_name: str,
        processor: Optional[BaseSyncProcessor] = None,
    ) -> None:
        meta_table_manager = MetaTableManager(self._connection, namespace, table_name)

        since = await meta_table_manager.last_sync_datetime()

        client = await IncrementalClientFactory(
            self._session, namespace, table_name, since
        ).get_client()

        if processor is None:
            processor = SyncProcessor(
                db_connection=self._connection,
                namespace=namespace,
                table_name=table_name,
                schema=client.table_schema,
            )

        await processor.prepare()

        await meta_table_manager.synchronize(client.table_data)
        await client.download(processor)

        async with self._connection.context() as conn:
            await conn.commit()
