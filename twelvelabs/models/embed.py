from __future__ import annotations

from typing import (
    List,
    Union,
    BinaryIO,
    Optional,
    Literal,
    Callable,
    Any,
    TYPE_CHECKING,
)
from pydantic import PrivateAttr, Field

from ._base import BaseModel, Object, RootModelList, PageInfo

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


class EmbeddingMediaMetadata(BaseModel):
    input_url: Optional[str] = None
    input_filename: Optional[str] = None


class Embedding(BaseModel):
    segments: Optional[List[SegmentEmbedding]] = None
    error_message: Optional[str] = None
    metadata: Optional[EmbeddingMediaMetadata] = None


class SegmentEmbedding(BaseModel):
    start_offset_sec: Optional[float] = None
    end_offset_sec: Optional[float] = None
    embedding_scope: Optional[str] = None
    embedding_option: Optional[str] = None
    embeddings_float: Optional[List[float]] = Field(default=None, alias="float")


class CreateEmbeddingsResult(BaseModel):
    model_name: str
    text_embedding: Optional[Embedding] = None
    image_embedding: Optional[Embedding] = None
    video_embedding: Optional[Embedding] = None
    audio_embedding: Optional[Embedding] = None

    class Config:
        # Disable the protected namespace restriction for model_name
        protected_namespaces = ()


class EmbeddingMetadata(BaseModel):
    input_url: Optional[str] = None
    input_filename: Optional[str] = None
    video_clip_length: Optional[int] = None
    video_embedding_scope: Optional[List[str]] = None
    duration: Optional[float] = None


class EmbeddingsTaskStatus(Object):
    model_name: str
    status: str
    metadata: Optional[EmbeddingMetadata] = None
    video_embedding: Optional[Embedding] = None

    class Config:
        # Disable the protected namespace restriction for model_name
        protected_namespaces = ()


class EmbeddingsTask(Object):
    _resource: EmbedTaskResource = PrivateAttr()
    model_name: str
    status: str
    video_embedding: Optional[Embedding] = None
    created_at: Optional[str] = None

    class Config:
        # Disable the protected namespace restriction for model_name
        protected_namespaces = ()

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


class EmbeddingsTaskListWithPagination(BaseModel):
    _resource: EmbedTaskResource = PrivateAttr()
    _origin_params: dict[str, Any] = PrivateAttr()
    data: RootModelList[EmbeddingsTask] = []
    page_info: PageInfo

    def __init__(
        self, resource: EmbedTaskResource, origin_params: dict[str, Any], **data
    ):
        super().__init__(**data)
        self._resource = resource
        self._origin_params = origin_params

    def __iter__(self):
        return self

    def __next__(self) -> RootModelList[EmbeddingsTask]:
        if self.page_info.page >= self.page_info.total_page:
            raise StopIteration
        params = self._origin_params
        params["page"] = self.page_info.page + 1
        res = self._resource.list_pagination(**params)
        self.page_info = res.page_info
        return res.data
