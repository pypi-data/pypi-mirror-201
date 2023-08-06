import logging
from typing import ClassVar


class LogFormatter(logging.Formatter):
    """Logging Formatter that distinguishes log levels and formats accordingly"""

    _default_format: ClassVar[str] = "%(asctime)s - %(levelname)s - %(message)s"
    _debug_format: ClassVar[str] = f"{_default_format} (%(filename)s:%(lineno)d)"

    def __init__(self, loglevel: int) -> None:
        log_format = (
            LogFormatter._debug_format
            if loglevel <= logging.DEBUG
            else LogFormatter._default_format
        )
        super().__init__(log_format)

    def format(self, record: logging.LogRecord) -> str:
        return super().format(record)
