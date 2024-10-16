from __future__ import annotations

from typing import List, Union, BinaryIO, Optional, Literal, Callable, TYPE_CHECKING
from pydantic import PrivateAttr, Field

from ._base import BaseModel, Object, RootModelList

if TYPE_CHECKING:
    from ..resources import EmbedTask as EmbedTaskResource


class CreateEmbeddingsTaskVideoParams:
    file: Union[str, BinaryIO, None]
    url: Optional[str]
    start_offset_sec: Optional[float]
    end_offset_sec: Optional[float]
    clip_length: Optional[int]
    scopes: Optional[List[Literal["clip", "video"]]]

    def __init__(
        self,
        file: Union[str, BinaryIO, None] = None,
        *,
        url: Optional[str] = None,
        start_offset_sec: Optional[float] = None,
        end_offset_sec: Optional[float] = None,
        clip_length: Optional[int] = None,
        scopes: Optional[List[Literal["clip", "video"]]] = None,
    ):
        self.file = file
        self.url = url
        self.start_offset_sec = start_offset_sec
        self.end_offset_sec = end_offset_sec
        self.clip_length = clip_length
        self.scopes = scopes


class Embedding(BaseModel):
    float: List[float]


class CreateEmbeddingsResult(BaseModel):
    engine_name: str
    text_embedding: Embedding


class EmbeddingsTaskStatus(Object):
    engine_name: str
    status: str


class VideoEmbedding(BaseModel):
    start_offset_sec: float
    end_offset_sec: float
    embedding_scope: str
    values: Optional[List[float]] = Field(default=None, alias="float")


class EmbeddingsTask(Object):
    _resource: EmbedTaskResource = PrivateAttr()
    engine_name: str
    status: str
    video_embeddings: Optional[RootModelList[VideoEmbedding]] = None

    def __init__(self, resource: EmbedTaskResource, **data):
        super().__init__(**data)
        self._resource = resource

    @property
    def done(self) -> bool:
        return self.status in ("ready", "failed")

    def retrieve(self, **kwargs) -> EmbeddingsTask:
        return self._resource.retrieve(self.id, **kwargs)

    def update_status(self, **kwargs) -> str:
        res = self._resource.status(self.id, **kwargs)
        self.status = res.status
        return self.status

    def wait_for_done(
        self,
        *,
        sleep_interval: float = 5.0,
        callback: Optional[Callable[[EmbeddingsTask], None]] = None,
        **kwargs,
    ) -> str:
        if sleep_interval <= 0:
            raise ValueError("sleep_interval must be greater than 0")
        while not self.done:
            self._resource._sleep(sleep_interval)
            try:
                self.update_status(**kwargs)
            except Exception as e:
                print(f"Retrieving status failed: {e}. Retrying..")
                continue
            if callback is not None:
                callback(self)
        return self.status
