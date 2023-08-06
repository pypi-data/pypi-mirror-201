from sqlalchemy import Connection, Inspector, MetaData, Table, inspect

from ..database.connection import DatabaseConnection
from ..database.database_errors import NonExistingTableError
from ..model.meta_table import MetatableManager


def _drop_table(db_connection: Connection, namespace: str, table_name: str) -> None:
    inspector: Inspector = inspect(db_connection)
    if not inspector.has_table(table_name=table_name, schema=namespace):
        raise NonExistingTableError(namespace, table_name)

    table_def = Table(table_name, MetaData(schema=namespace))
    table_def.drop(bind=db_connection)


async def drop_db(connection_string: str, namespace: str, table_name: str) -> None:
    async with DatabaseConnection(connection_string) as db_connection:
        await db_connection.run_sync(lambda c: _drop_table(c, namespace, table_name))
        await MetatableManager(db_connection, namespace, table_name).drop()
        await db_connection.commit()
