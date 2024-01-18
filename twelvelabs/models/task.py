from __future__ import annotations

from typing import Optional, Dict, Any, Callable, TYPE_CHECKING
from pydantic import PrivateAttr

from ._base import ObjectWithTimestamp, BaseModel

if TYPE_CHECKING:
    from ..resources import Task as TaskResource


class Task(ObjectWithTimestamp):
    _resource: TaskResource = PrivateAttr()
    index_id: str
    estimated_time: Optional[str] = None
    status: str
    metadata: Dict[str, Any]
    process: Optional[Dict[str, Any]] = None

    def __init__(self, resource: TaskResource, **data):
        super().__init__(**data)
        self._resource = resource

    # Task related methods

    @property
    def done(self) -> bool:
        return self.status in ("ready", "failed")

    def retrieve(self, **kwargs) -> Task:
        return self._resource.retrieve(self.id, **kwargs)

    def delete(self, **kwargs) -> None:
        return self._resource.delete(self.id, **kwargs)

    def wait_for_done(
        self,
        *,
        sleep_interval: float = 5.0,
        callback: Optional[Callable[[Task], None]],
        **kwargs,
    ) -> Task:
        if sleep_interval <= 0:
            raise ValueError("sleep_interval must be greater than 0")
        while not self.done:
            self._resource._sleep(sleep_interval)
            task = self.retrieve(**kwargs)
            self.estimated_time = task.estimated_time
            self.status = task.status
            self.metadata = task.metadata
            self.process = task.process
            if callback is not None:
                callback(self)
        return self


class TaskStatus(BaseModel):
    index_id: str
    ready: int
    validating: int
    pending: int
    failed: int
    total_result: int
