import asyncio
import errno
import logging
import os
import sys
import traceback

from .arguments import Arguments
from .commands.commands import (
    DapCommandRegistrar,
    IncrementalCommandRegistrar,
    ListCommandRegistrar,
    SchemaCommandRegistrar,
    SnapshotCommandRegistrar,
)
from .commands.commonargs import (
    BaseUrlArgumentRegistrar,
    HelpArgumentRegistrar,
    LogLevelArgumentRegistrar,
    OAuthCredentialsArgumentRegistrar,
)
from .commands.dbargs import DatabaseConnectionStringArgumentRegistrar
from .commands.dropdb_command import DropDBCommandRegistrar
from .commands.initdb_command import InitDBCommandRegistrar
from .commands.queryargs import (
    FormatArgumentRegistrar,
    NamespaceArgumentRegistrar,
    OutputDirectoryArgumentRegistrar,
    TableArgumentRegistrar,
)
from .commands.syncdb_command import SyncDBCommandRegistrar
from .commands.timestampargs import SinceArgumentRegistrar, UntilArgumentRegistrar
from .dap_error import OperationError
from .log import LogFormatter

dapCommand = DapCommandRegistrar(
    arguments=[
        BaseUrlArgumentRegistrar(),
        OAuthCredentialsArgumentRegistrar(),
        LogLevelArgumentRegistrar(),
        HelpArgumentRegistrar(),
    ],
    subcommands=[
        # Definition of the 'snapshot' command
        SnapshotCommandRegistrar(
            [
                TableArgumentRegistrar(),
                FormatArgumentRegistrar(),
                OutputDirectoryArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
            ]
        ),
        # Definition of the 'incremental' command
        IncrementalCommandRegistrar(
            [
                TableArgumentRegistrar(),
                FormatArgumentRegistrar(),
                OutputDirectoryArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
                SinceArgumentRegistrar(),
                UntilArgumentRegistrar(),
            ]
        ),
        # Definition of the 'list' command
        ListCommandRegistrar([NamespaceArgumentRegistrar()]),
        # Definition of the 'schema' command
        SchemaCommandRegistrar(
            [
                NamespaceArgumentRegistrar(),
                TableArgumentRegistrar(),
                OutputDirectoryArgumentRegistrar(),
            ]
        ),
        # Definition of the 'initdb' command
        InitDBCommandRegistrar(
            [
                TableArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
                DatabaseConnectionStringArgumentRegistrar(),
            ]
        ),
        # Definition of the 'syncdb' command
        SyncDBCommandRegistrar(
            [
                TableArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
                DatabaseConnectionStringArgumentRegistrar(),
            ]
        ),
        # Definition of the 'dropdb' command
        DropDBCommandRegistrar(
            [
                TableArgumentRegistrar(),
                NamespaceArgumentRegistrar(),
                DatabaseConnectionStringArgumentRegistrar(),
            ]
        ),
    ],
)


def main() -> None:
    parser = dapCommand.register()

    args = Arguments()
    if parser:
        parser.parse_args(namespace=args)

    logging.basicConfig(
        level=getattr(logging, args.loglevel.upper(), logging.INFO),
    )
    loglevel = logging.root.getEffectiveLevel()
    logging.root.handlers[0].setFormatter(LogFormatter(loglevel))

    asyncio.run(dapCommand.execute(args))


def console_entry() -> None:
    # propagate exceptions to interactive development environment
    if os.getenv("TERM_PROGRAM") == "vscode":
        main()
        return

    # handle exceptions for production deployments
    try:
        main()
    except OperationError as e:
        logging.error(
            f"An exception occurred while executing the command: {e.message} ({e.uuid})"
        )
        logging.exception(e)
        sys.exit(errno.EIO)
    except NotImplementedError as e:
        logging.error(e)
        sys.exit(errno.ENOSYS)
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        sys.exit(errno.EINTR)
    except Exception as e:
        # Handle any other exception in similar way
        logging.debug(traceback.format_exc())
        logging.error(e)
        sys.exit(errno.EIO)


if __name__ == "__main__":
    console_entry()
