import asyncio
from typing import Any, Callable, Dict, Optional

from pydantic import PrivateAttr

from .models import Object


class Task(Object):
    _client = PrivateAttr()
    index_id: str
    estimated_time: Optional[str]
    status: str
    metadata: Dict[str, Any]
    process: Optional[Dict[str, Any]]  # TODO: does it exist?

    def __init__(self, client, **data):
        super().__init__(**data)
        self._client = client

    @property
    def done(self) -> bool:
        return self.status in ("ready", "failed")

    async def get(self, **kwargs) -> "Task":
        return await self._client.get_task(self.id, **kwargs)

    async def delete(self, **kwargs):
        await self.client.delete_task(self.id, **kwargs)

    async def wait(
        self,
        cb: Callable[["Task"], None],
        sleep_interval: float = 5.0,
        **kwargs,
    ) -> "Task":
        while not self.done:
            await asyncio.sleep(sleep_interval)
            task = await self.get(**kwargs)
            self.estimated_time = task.estimated_time
            self.status = task.status
            self.metadata = task.metadata
            self.process = task.process
            cb(self)
        return self
