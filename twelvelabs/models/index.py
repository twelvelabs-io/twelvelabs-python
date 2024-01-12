from typing import List, Optional
from pydantic import Field, PrivateAttr

from ._base import BaseModel, ObjectWithTimestamp
from ..resource import APIResource


class Engine(BaseModel):
    name: str = Field(alias="engine_name")
    options: List[str] = Field(alias="engine_options")
    addons: Optional[List[str]] = None


class Index(ObjectWithTimestamp):
    _client = PrivateAttr()
    name: str = Field(alias="index_name")
    # engine_id: str # v1.1
    engines: List[Engine]
    # options: List[str] = Field(alias="index_options") # v1.1
    # addons: Optional[List[str]] # v1.1
    video_count: int
    total_duration: float
    expires_at: Optional[str] = None

    def __init__(self, client: APIResource, **data):
        super().__init__(**data)
        self._client = client

    # index related apis
