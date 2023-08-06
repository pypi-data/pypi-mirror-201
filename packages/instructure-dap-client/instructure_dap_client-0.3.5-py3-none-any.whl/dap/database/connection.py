import types
from typing import Optional, Type

from asyncpg import InvalidCatalogNameError
from sqlalchemy import URL, make_url
from sqlalchemy.exc import NoSuchModuleError
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from .database_errors import DatabaseConnectionError, DatabaseProtocolError


def _specify_database_driver(original_url: str) -> URL:
    try:
        url = make_url(original_url)
        dialect = url.get_dialect().name
        driver = url.get_dialect().driver
        updated_driver = _get_driver_for_dialect(dialect)
        if driver != updated_driver:
            url = url.set(drivername=f"{dialect}+{updated_driver}")
        return url
    except NoSuchModuleError as exc:
        raise DatabaseProtocolError(
            f"unknown database protocol: {url.drivername}"
        ) from exc


def _get_driver_for_dialect(dialect: str) -> str:
    dialect_to_driver_mapping = {"postgresql": "asyncpg"}
    driver = dialect_to_driver_mapping.get(dialect, None)
    if driver is not None:
        return driver
    else:
        raise ValueError(f"SQLAlchemy dialect not supported: {dialect}")


class DatabaseConnection:
    _connection: AsyncConnection

    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    async def __aenter__(self) -> AsyncConnection:
        try:
            database_url = _specify_database_driver(self._connection_string)
            engine = create_async_engine(database_url)
            self._connection = engine.connect()

            return await self._connection.__aenter__()
        except (InvalidCatalogNameError, OSError) as e:
            # in this case either host/port or database name is invalid
            raise DatabaseConnectionError(f"database connection error: {e}") from e

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> None:
        await self._connection.__aexit__(exc_type, exc_val, exc_tb)
