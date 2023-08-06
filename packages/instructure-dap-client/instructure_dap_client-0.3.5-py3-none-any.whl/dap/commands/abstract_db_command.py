import logging

from ..database.connection import DatabaseConnection
from .base import Arguments, CommandRegistrar


class AbstractDbCommandRegistrar(CommandRegistrar):
    async def _before_execute(self, args: Arguments) -> None:
        logging.debug(f"Checking connection to {args.connection_string}")
        async with DatabaseConnection(args.connection_string):
            # simply open and close connection to check validity
            pass
