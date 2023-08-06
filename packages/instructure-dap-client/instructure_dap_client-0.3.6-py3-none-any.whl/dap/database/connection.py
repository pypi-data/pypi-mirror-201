import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

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
    "Parameters of a connection to a relational database where data is synchronized to."

    connection_string: str

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    @asynccontextmanager
    async def open(self) -> AsyncIterator["DatabaseSession"]:
        try:
            database_url = _specify_database_driver(self.connection_string)
            engine = create_async_engine(database_url)
            async with engine.connect() as conn:
                yield DatabaseSession(conn)

        except (InvalidCatalogNameError, OSError) as e:
            # in this case either host/port or database name is invalid
            raise DatabaseConnectionError(f"database connection error: {e}") from e


class DatabaseSession:
    "An open database connection to a relational database where data is synchronized to."

    connection: AsyncConnection
    _lock: asyncio.Lock

    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def context(self) -> AsyncIterator["AsyncConnection"]:
        async with self._lock:
            yield self.connection
