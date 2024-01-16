from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING
from pydantic import PrivateAttr

from ._base import ObjectWithTimestamp, BaseModel

if TYPE_CHECKING:
    from ..resources import Video as VideoResource


class Video(ObjectWithTimestamp):
    _resource: VideoResource = PrivateAttr()
    # index_id: str
    indexed_at: Optional[str]
    metadata: Dict[str, Any]

    def __init__(self, resource: VideoResource, **data):
        super().__init__(**data)
        self._resource = resource

    # video related apis


class VideoValue(BaseModel):
    start: float
    end: float
    value: str
