import abc
from dataclasses import dataclass
from types import TracebackType
from typing import Optional, Type

from ..dap_types import JobID, ObjectID
from ..type_conversion import JsonRecord


@dataclass(frozen=True)
class ContextAwareObject:
    "Provides information about the context in which the records are processed."

    id: ObjectID
    index: int
    total_count: int
    job_id: JobID

    def __str__(self) -> str:
        return f"[object {self.index + 1}/{self.total_count} - job {self.job_id}]"


class BaseBatch(abc.ABC):
    "Base class for replicating data acquired from DAP API in a relational database."

    @abc.abstractmethod
    async def process(self, record: JsonRecord) -> None:
        """
        Processes a single record.

        :param record: JSON object to process.
        """
        ...

    @abc.abstractmethod
    async def __aenter__(self) -> "BaseBatch":
        ...

    @abc.abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        ...


class BaseProcessor(abc.ABC):
    @abc.abstractmethod
    async def prepare(self) -> None:
        """
        Prepares for processing of a stream of records.

        For initializing a database, this would issue SQL `CREATE TABLE` statements that records about to be received
        might be inserted into.

        For synchronizing a database, this would check whether the table exists that is about to be synchronized.
        """
        ...

    @abc.abstractmethod
    def batch(self, obj: ContextAwareObject) -> "BaseBatch":
        """
        Starts processing a batch of records.

        :param obj: Object that the records belong to. This helps trace records back to their source.
        """
        ...

    @abc.abstractmethod
    async def close(self) -> None:
        """
        Ends processing records. Invoked after all records have been processed.
        """
        ...


class BaseInitProcessor(BaseProcessor):
    "Base class for initializing a table in relational database with data acquired from DAP API."


class BaseSyncProcessor(BaseProcessor):
    "Base class for synchronizing an existing table in a relational database with data from DAP API."
