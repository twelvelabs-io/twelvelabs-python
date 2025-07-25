from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING, Union, BinaryIO, Literal, Dict, Any
from pydantic import Field, PrivateAttr

from ._base import ModelMixin, BaseModel, ObjectWithTimestamp, PageInfo, RootModelList

if TYPE_CHECKING:
    from ..resources import Index as IndexResource
    from . import Task, TaskStatus, SearchResult, Video, VideoListWithPagination


class Model(BaseModel):
    name: str = Field(alias="model_name")
    # conversation, text_in_video, and logo are to keep backward compatibility with the old models
    options: List[
        Literal["visual", "audio", "conversation", "text_in_video", "logo"]
    ] = Field(alias="model_options")
    addons: Optional[List[str]] = None
    finetuned: Optional[bool] = None

    class Config:
        # Disable the protected namespace restriction for options
        protected_namespaces = ()


class Index(ObjectWithTimestamp):
    _resource: IndexResource = PrivateAttr()
    name: str = Field(alias="index_name")
    models: RootModelList[Model]
    video_count: int
    total_duration: float
    expires_at: Optional[str] = None

    def __init__(self, resource: IndexResource, **data):
        super().__init__(**data)
        self._resource = resource

    # Index related methods

    def retrieve(self, **kwargs) -> Index:
        return self._resource.retrieve(self.id, **kwargs)

    def update(self, name: str, **kwargs) -> None:
        return self._resource.update(self.id, name, **kwargs)

    def delete(self, **kwargs) -> None:
        return self._resource.delete(self.id, **kwargs)

    # Task related methods

    def create_task(
        self,
        *,
        file: Union[str, BinaryIO, None] = None,
        url: Optional[str] = None,
        transcription_file: Union[str, BinaryIO, None] = None,
        transcription_url: Optional[str] = None,
        **kwargs,
    ) -> Task:
        return self._resource._client.task.create(
            self.id,
            file=file,
            url=url,
            transcript_file=transcription_file,
            transcription_url=transcription_url,
            **kwargs,
        )

    def task_status(self, **kwargs) -> TaskStatus:
        return self._resource._client.task.status(self.id, **kwargs)

    # Video related methods
    def list_video(
        self,
        *,
        filename: Optional[str] = None,
        size: Optional[Union[int, Dict[str, int]]] = None,
        width: Optional[Union[int, Dict[str, int]]] = None,
        height: Optional[Union[int, Dict[str, int]]] = None,
        duration: Optional[Union[int, Dict[str, int]]] = None,
        fps: Optional[Union[int, Dict[str, int]]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> RootModelList[Video]:
        return self._resource.video.list(
            self.id,
            filename=filename,
            size=size,
            width=width,
            height=height,
            duration=duration,
            fps=fps,
            user_metadata=user_metadata,
            created_at=created_at,
            updated_at=updated_at,
            page=page,
            page_limit=page_limit,
            sort_by=sort_by,
            sort_option=sort_option,
            **kwargs,
        )

    def list_video_pagination(
        self,
        *,
        filename: Optional[str] = None,
        size: Optional[Union[int, Dict[str, int]]] = None,
        width: Optional[Union[int, Dict[str, int]]] = None,
        height: Optional[Union[int, Dict[str, int]]] = None,
        duration: Optional[Union[int, Dict[str, int]]] = None,
        fps: Optional[Union[int, Dict[str, int]]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> VideoListWithPagination:
        return self._resource.video.list_pagination(
            self.id,
            filename=filename,
            size=size,
            width=width,
            height=height,
            duration=duration,
            fps=fps,
            user_metadata=user_metadata,
            created_at=created_at,
            updated_at=updated_at,
            page=page,
            page_limit=page_limit,
            sort_by=sort_by,
            sort_option=sort_option,
            **kwargs,
        )

    # Search related methods

    def query(
        self,
        options: Literal["visual", "audio"],
        *,
        query_text: str = None,
        query_media_type: Literal["image"] = None,
        query_media_file: Union[str, BinaryIO, None] = None,
        query_media_url: str = None,
        group_by: Optional[Literal["video", "clip"]] = None,
        threshold: Optional[Literal["high", "medium", "low", "none"]] = None,
        operator: Optional[Literal["or", "and"]] = None,
        filter: Optional[Dict[str, Any]] = None,
        page_limit: Optional[int] = None,
        sort_option: Optional[Literal["score", "clip_count"]] = None,
        adjust_confidence_level: Optional[float] = None,
        **kwargs,
    ) -> SearchResult:
        return self._resource._client.search.query(
            self.id,
            options,
            query_text=query_text,
            query_media_type=query_media_type,
            query_media_file=query_media_file,
            query_media_url=query_media_url,
            group_by=group_by,
            threshold=threshold,
            operator=operator,
            filter=filter,
            page_limit=page_limit,
            sort_option=sort_option,
            adjust_confidence_level=adjust_confidence_level,
            **kwargs,
        )


class IndexListWithPagination(ModelMixin, BaseModel):
    _resource: IndexResource = PrivateAttr()
    _origin_params: Dict[str, Any] = PrivateAttr()
    data: List[Index] = []
    page_info: PageInfo

    def __init__(self, resource: IndexResource, origin_params: Dict[str, Any], **data):
        super().__init__(**data)
        self._resource = resource
        self._origin_params = origin_params

    def __iter__(self):
        return self

    def __next__(self) -> List[Index]:
        if self.page_info.page >= self.page_info.total_page:
            raise StopIteration
        params = self._origin_params
        params["page"] = self.page_info.page + 1
        res = self._resource.list_pagination(**params)
        self.page_info = res.page_info
        return res.data
