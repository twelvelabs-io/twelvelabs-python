from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Dict, Any, List, Union, Literal
from pydantic import PrivateAttr

from ._base import ObjectWithTimestamp, BaseModel

if TYPE_CHECKING:
    from ..resources import Video as VideoResource
    from . import (
        GeneratorGistResult,
        GenerateSummarizeResult,
        GenerateOpenEndedTextResult,
    )


class VideoMetadata(BaseModel):
    filename: str
    duration: float
    fps: float
    width: int
    height: int
    size: int


class VideoValue(BaseModel):
    start: float
    end: float
    value: str


class Video(ObjectWithTimestamp):
    _resource: VideoResource = PrivateAttr()
    _index_id: str = PrivateAttr()
    indexed_at: Optional[str] = None
    metadata: VideoMetadata

    def __init__(self, resource: VideoResource, index_id: str, **data):
        self._resource = resource
        self._index_id = index_id
        super().__init__(**data)

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
    ) -> List[VideoValue]:
        return self._resource._client.index.video.transcription(
            self._index_id, self.id, start=start, end=end, **kwargs
        )

    def text_in_video(
        self, *, start: Optional[float] = None, end: Optional[float] = None, **kwargs
    ) -> List[VideoValue]:
        return self._resource._client.index.video.text_in_video(
            self._index_id, self.id, start=start, end=end, **kwargs
        )

    def logo(
        self, *, start: Optional[float] = None, end: Optional[float] = None, **kwargs
    ) -> List[VideoValue]:
        return self._resource._client.index.video.logo(
            self._index_id, self.id, start=start, end=end, **kwargs
        )

    def thumbnail(self, *, time: Optional[float] = None, **kwargs) -> List[VideoValue]:
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