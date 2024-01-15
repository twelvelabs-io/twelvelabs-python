from typing import Optional, Dict, Any
from pydantic import PrivateAttr

from ._base import ObjectWithTimestamp, BaseModel
from ..resource import APIResource


class Task(ObjectWithTimestamp):
    _client = PrivateAttr()
    index_id: str
    estimated_time: Optional[str]
    status: str
    metadata: Dict[str, Any]
    process: Optional[Dict[str, Any]]

    def __init__(self, client: APIResource, **data):
        super().__init__(**data)
        self._client = client

    # task related apis


class TaskStatus(BaseModel):
    index_id: str
    ready: int
    validating: int
    pending: int
    failed: int
    total_result: int
