from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Dict, Any, List, Union, Literal
from pydantic import PrivateAttr, Extra

from ._base import ObjectWithTimestamp, BaseModel, ModelMixin, PageInfo, RootModelList

if TYPE_CHECKING:
    from ..resources import Video as VideoResource
    from . import (
        GeneratorGistResult,
        GenerateSummarizeResult,
        GenerateOpenEndedTextResult,
        Embedding,
    )


class VideoMetadata(BaseModel):
    filename: str
    duration: float
    fps: float
    width: int
    height: int
    size: int

    class Config:
        extra = Extra.allow  # This allows extra fields


class VideoHLS(BaseModel):
    video_url: Optional[str] = None
    thumbnail_urls: Optional[List[str]] = None
    status: Optional[str] = None
    updated_at: Optional[str] = None


class VideoValue(BaseModel):
    start: float
    end: float
    value: str


class VideoSource(BaseModel):
    type: str
    name: str
    url: Optional[str] = None


class Video(ObjectWithTimestamp):
    _resource: VideoResource = PrivateAttr()
    _index_id: str = PrivateAttr()
    metadata: VideoMetadata
    hls: Optional[VideoHLS] = None
    source: Optional[VideoSource] = None
    indexed_at: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
    embedding: Optional[Embedding] = None

    def __init__(self, resource: VideoResource, index_id: str, **data):
        super().__init__(**data)
        self._resource = resource
        self._index_id = index_id

    # Video related methods

    def update(
        self,
        *,
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        return self._resource._client.index.video.update(
            self._index_id, self.id, title=title, metadata=metadata, **kwargs
        )

    def delete(
        self,
        **kwargs,
    ) -> None:
        return self._resource._client.index.video.delete(
            self._index_id, self.id, **kwargs
        )

    def transcription(
        self, *, start: Optional[float] = None, end: Optional[float] = None, **kwargs
    ) -> RootModelList[VideoValue]:
        return self._resource._client.index.video.transcription(
            self._index_id, self.id, start=start, end=end, **kwargs
        )

    def text_in_video(
        self, *, start: Optional[float] = None, end: Optional[float] = None, **kwargs
    ) -> RootModelList[VideoValue]:
        return self._resource._client.index.video.text_in_video(
            self._index_id, self.id, start=start, end=end, **kwargs
        )

    def logo(
        self, *, start: Optional[float] = None, end: Optional[float] = None, **kwargs
    ) -> RootModelList[VideoValue]:
        return self._resource._client.index.video.logo(
            self._index_id, self.id, start=start, end=end, **kwargs
        )

    def thumbnail(self, *, time: Optional[float] = None, **kwargs) -> str:
        return self._resource._client.index.video.thumbnail(
            self._index_id, self.id, time=time, **kwargs
        )

    # Generate relate methods

    def generate_gist(
        self, types: List[Union[str, Literal["topic", "hashtag", "title"]]], **kwargs
    ) -> GeneratorGistResult:
        return self._resource._client.generate.gist(self.id, types, **kwargs)

    def generate_summarize(
        self,
        type: Union[str, Literal["summary", "chapter", "highlight"]],
        *,
        prompt: Optional[str] = None,
        **kwargs,
    ) -> GenerateSummarizeResult:
        return self._resource._client.generate.summarize(
            self.id, type, prompt=prompt, **kwargs
        )

    def generate_text(
        self,
        prompt: Optional[str] = None,
        **kwargs,
    ) -> GenerateOpenEndedTextResult:
        return self._resource._client.generate.text(
            self.id, type, prompt=prompt, **kwargs
        )


class VideoListWithPagination(ModelMixin, BaseModel):
    _resource: VideoResource = PrivateAttr()
    _origin_params: Dict[str, Any] = PrivateAttr()
    data: RootModelList[Video] = []
    page_info: PageInfo

    def __init__(self, resource: VideoResource, origin_params: Dict[str, Any], **data):
        super().__init__(**data)
        self._resource = resource
        self._origin_params = origin_params

    def __iter__(self):
        return self

    def __next__(self) -> RootModelList[Video]:
        if self.page_info.page >= self.page_info.total_page:
            raise StopIteration
        params = self._origin_params
        params["page"] = self.page_info.page + 1
        res = self._resource.list_pagination(**params)
        self.page_info = res.page_info
        return res.data
