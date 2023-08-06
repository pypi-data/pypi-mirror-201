from typing import Optional

from sqlalchemy.ext.asyncio import AsyncConnection

from ..api import DAPSession
from ..database.base_processor import BaseSyncProcessor, BaseInitProcessor
from ..database.init_processor import InitProcessor
from ..database.sync_processor import SyncProcessor
from ..downloader import IncrementalClientFactory, SnapshotClientFactory
from ..model.meta_table import MetatableManager


class SQLReplicator:
    """
    Encapsulates logic that replicates changes acquired from DAP API in a SQL database.
    """

    def __init__(self, session: DAPSession, connection: AsyncConnection) -> None:
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

        await MetatableManager(self._connection, namespace, table_name).initialize(
            table_schema=client.table_schema, table_data=client.table_data
        )

        await client.download(processor)

        await self._connection.commit()

    async def synchronize(
        self,
        namespace: str,
        table_name: str,
        processor: Optional[BaseSyncProcessor] = None,
    ) -> None:
        metatable_manager = MetatableManager(self._connection, namespace, table_name)

        since = await metatable_manager.last_sync_datetime()

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

        await metatable_manager.synchronize(client.table_data)
        await client.download(processor)
        await self._connection.commit()
