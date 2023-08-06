from sqlalchemy import Connection, Inspector, MetaData, Table, inspect

from ..database.connection import DatabaseConnection
from ..database.database_errors import NonExistingTableError
from ..model.meta_table import MetaTableManager


def _drop_table(db_connection: Connection, namespace: str, table_name: str) -> None:
    inspector: Inspector = inspect(db_connection)
    if not inspector.has_table(table_name=table_name, schema=namespace):
        raise NonExistingTableError(namespace, table_name)

    table_def = Table(table_name, MetaData(schema=namespace))
    table_def.drop(bind=db_connection)


async def drop_db(connection_string: str, namespace: str, table_name: str) -> None:
    async with DatabaseConnection(connection_string).open() as db_connection:
        async with db_connection.context() as conn:
            await conn.run_sync(lambda c: _drop_table(c, namespace, table_name))

        await MetaTableManager(db_connection, namespace, table_name).drop()

        async with db_connection.context() as conn:
            await conn.commit()
