from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING, Union, BinaryIO, Literal, Dict, Any
from pydantic import Field, PrivateAttr

from ._base import ModelMixin, BaseModel, ObjectWithTimestamp, PageInfo, RootModelList

if TYPE_CHECKING:
    from ..resources import Index as IndexResource
    from . import Task, TaskStatus, SearchResult, Video, VideoListWithPagination


class Engine(BaseModel):
    name: str = Field(alias="engine_name")
    options: List[str] = Field(alias="engine_options")
    addons: Optional[List[str]] = None
    finetuned: Optional[bool] = None


class Index(ObjectWithTimestamp):
    _resource: IndexResource = PrivateAttr()
    name: str = Field(alias="index_name")
    # engine_id: str # v1.1
    engines: RootModelList[Engine]
    # options: List[str] = Field(alias="index_options") # v1.1
    # addons: Optional[List[str]] # v1.1
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
        language: Optional[str] = None,
        **kwargs,
    ) -> Task:
        return self._resource._client.task.create(
            self.id,
            file=file,
            url=url,
            transcript_file=transcription_file,
            transcription_url=transcription_url,
            language=language,
            **kwargs,
        )

    def task_status(self, **kwargs) -> TaskStatus:
        return self._resource._client.task.status(self.id, **kwargs)

    def task_external_provider(self, url: str, **kwargs):
        return self._resource._client.task.external_provider(self.id, url, **kwargs)

    # Video related methods
    def list_video(
        self,
        *,
        id: Optional[str] = None,
        filename: Optional[str] = None,
        size: Optional[Union[str, Dict[str, str]]] = None,
        width: Optional[Union[str, Dict[str, str]]] = None,
        height: Optional[Union[str, Dict[str, str]]] = None,
        duration: Optional[Union[str, Dict[str, str]]] = None,
        fps: Optional[Union[str, Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        indexed_at: Optional[Union[str, Dict[str, str]]] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> RootModelList[Video]:
        return self._resource.video.list(
            self.id,
            id=id,
            filename=filename,
            size=size,
            width=width,
            height=height,
            duration=duration,
            fps=fps,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
            indexed_at=indexed_at,
            page=page,
            page_limit=page_limit,
            sort_by=sort_by,
            sort_option=sort_option,
            **kwargs,
        )

    def list_video_pagination(
        self,
        *,
        id: Optional[str] = None,
        filename: Optional[str] = None,
        size: Optional[Union[str, Dict[str, str]]] = None,
        width: Optional[Union[str, Dict[str, str]]] = None,
        height: Optional[Union[str, Dict[str, str]]] = None,
        duration: Optional[Union[str, Dict[str, str]]] = None,
        fps: Optional[Union[str, Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        indexed_at: Optional[Union[str, Dict[str, str]]] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> VideoListWithPagination:
        return self._resource.video.list_pagination(
            self.id,
            id=id,
            filename=filename,
            size=size,
            width=width,
            height=height,
            duration=duration,
            fps=fps,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
            indexed_at=indexed_at,
            page=page,
            page_limit=page_limit,
            sort_by=sort_by,
            sort_option=sort_option,
            **kwargs,
        )

    # Search related methods

    def query(
        self,
        query: str,
        options: List[
            Union[str, Literal["visual", "conversation", "text_in_video", "logo"]]
        ],
        *,
        group_by: Optional[Union[str, Literal["video", "clip"]]] = None,
        threshold: Optional[Union[str, Literal["high", "medium", "low"]]] = None,
        operator: Optional[Union[str, Literal["or", "and"]]] = None,
        conversation_option: Optional[
            Union[str, Literal["semantic", "exact_match"]]
        ] = None,
        filter: Optional[Dict[str, Any]] = None,
        page_limit: Optional[int] = None,
        sort_option: Optional[Union[str, Literal["score", "clip_count"]]] = None,
        **kwargs,
    ) -> SearchResult:
        return self._resource._client.search.query(
            self.id,
            query,
            options,
            group_by=group_by,
            threshold=threshold,
            operator=operator,
            conversation_option=conversation_option,
            filter=filter,
            page_limit=page_limit,
            sort_option=sort_option,
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
