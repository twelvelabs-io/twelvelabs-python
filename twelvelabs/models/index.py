from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from pydantic import Field, PrivateAttr

from ._base import BaseModel, ObjectWithTimestamp

if TYPE_CHECKING:
    from ..resources import Index as IndexResource


class Engine(BaseModel):
    name: str = Field(alias="engine_name")
    options: List[str] = Field(alias="engine_options")
    addons: Optional[List[str]] = None


class Index(ObjectWithTimestamp):
    _resource: IndexResource = PrivateAttr()
    name: str = Field(alias="index_name")
    # engine_id: str # v1.1
    engines: List[Engine]
    # options: List[str] = Field(alias="index_options") # v1.1
    # addons: Optional[List[str]] # v1.1
    video_count: int
    total_duration: float
    expires_at: Optional[str] = None

    def __init__(self, resource: IndexResource, **data):
        super().__init__(**data)
        self._resource = resource

    # index related apis
