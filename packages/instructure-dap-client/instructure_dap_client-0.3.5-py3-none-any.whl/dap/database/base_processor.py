import abc
from dataclasses import dataclass

from ..dap_types import JobID, ObjectID
from ..type_conversion import JsonRecord


@dataclass(frozen=True)
class ContextAwareObject:
    id: ObjectID
    index: int
    total_count: int
    job_id: JobID

    def __str__(self) -> str:
        return f"[object {self.index + 1}/{self.total_count} - job {self.job_id}]"


class BaseInitProcessor(abc.ABC):
    @abc.abstractmethod
    async def prepare(self) -> None:
        """
        Prepares processing of records.
        For example, it might issue SQL `CREATE TABLE` statements that records about to be received might be inserted into.
        """
        ...

    @abc.abstractmethod
    async def process(self, record: JsonRecord, obj: ContextAwareObject) -> None:
        """
        Processes records. Object parameter helps with identification.

        :param record: JSON object to process.
        :param obj: Object that the record belongs to.
        """
        ...

    @abc.abstractmethod
    async def close(self) -> None:
        """
        Ends the operation. Invoked after the function `process` has been called for each item.
        """
        ...


class BaseSyncProcessor(abc.ABC):
    @abc.abstractmethod
    async def prepare(self) -> None:
        """
        Prepares processing of records.
        For example, it might check whether table exist that is required to be synchronized.
        """
        ...

    @abc.abstractmethod
    async def process_upsert(self, record: JsonRecord, obj: ContextAwareObject) -> None:
        """
        Processes record that is upsert.

        :param record: JSON record to process.
        :param obj: Object that the record belongs to.
        """
        ...

    @abc.abstractmethod
    async def process_delete(self, record: JsonRecord, obj: ContextAwareObject) -> None:
        """
        Processes deletion.

        :param record: JSON record to process.
        :param obj: Object that the record belongs to.
        """
        ...

    @abc.abstractmethod
    async def close(self) -> None:
        """
        Ends the operation. Invoked after the function `process` has been called for each item.
        """
        ...
