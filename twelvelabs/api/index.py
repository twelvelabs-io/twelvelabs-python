import asyncio
from typing import Any, BinaryIO, Dict, List, Optional, Tuple, Union

from pydantic import Field, PrivateAttr

from twelvelabs.api.classify import BulkClassifyResult

from .models import ClassifyLabel, Object, VideoFile
from .search import SearchResult
from .task import Task
from .video import Video


class Index(Object):
    _client = PrivateAttr()
    name: str = Field(alias="index_name")
    engine_id: str
    options: List[str] = Field(alias="index_options")
    addons: Optional[List[str]]
    video_count: int
    total_duration: float

    def __init__(self, client, **data):
        super().__init__(**data)
        self._client = client

    async def update(self, *, name: str, **kwargs):
        await self._client.update_index(self.id, name=name, **kwargs)

    async def delete(self, **kwargs):
        await self._client.delete_index(self.id, **kwargs)

    async def upload_video(
        self,
        *,
        file: Union[str, BinaryIO, None] = None,
        url: Optional[str] = None,
        transcription_file: Union[str, BinaryIO, None] = None,
        transcription_url: Optional[str] = None,
        language: Optional[str] = None,
        **kwargs,
    ) -> Task:
        return await self._client.upload_video(
            self.id,
            file=file,
            url=url,
            transcription_file=transcription_file,
            transcription_url=transcription_url,
            language=language,
            **kwargs,
        )

    async def upload_videos(self, videos: List[VideoFile], **kwargs) -> List[Task]:
        return await self._client.upload_videos(self.id, videos, **kwargs)

    async def list_tasks(
        self,
        *,
        id: Optional[str] = None,
        filename: Optional[str] = None,
        duration: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        estimated_time: Optional[str] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> Tuple[List[Task], int, int]:
        return await self._client.list_tasks(
            index_id=self.id,
            id=id,
            filename=filename,
            duration=duration,
            width=width,
            height=height,
            created_at=created_at,
            updated_at=updated_at,
            estimated_time=estimated_time,
            page=page,
            page_limit=page_limit,
            sort_by=sort_by,
            sort_option=sort_option,
            **kwargs,
        )

    async def get_tasks(
        self,
        *,
        id: Optional[str] = None,
        filename: Optional[str] = None,
        duration: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        estimated_time: Optional[str] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> List[Task]:
        return await self._client.get_tasks(
            index_id=self.id,
            id=id,
            filename=filename,
            duration=duration,
            width=width,
            height=height,
            created_at=created_at,
            updated_at=updated_at,
            estimated_time=estimated_time,
            page=page,
            page_limit=page_limit,
            sort_by=sort_by,
            sort_option=sort_option,
            **kwargs,
        )

    async def get_task(self, id: str, **kwargs) -> Task:
        return await self._client.get_task(id, **kwargs)

    async def status(self, **kwargs) -> Dict[str, Any]:
        return await self._client.tasks_status(self.id, **kwargs)

    async def list_videos(
        self,
        *,
        id: Optional[str] = None,
        filename: Optional[str] = None,
        size: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        duration: Optional[float] = None,
        fps: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        indexed_at: Optional[str] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> Tuple[List[Video], int, int]:
        return await self._client.list_videos(
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

    async def get_videos(
        self,
        *,
        id: Optional[str] = None,
        filename: Optional[str] = None,
        size: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        duration: Optional[float] = None,
        fps: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        indexed_at: Optional[str] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> List[Video]:
        return await self._client.get_videos(
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

    async def get_video(self, id: str, **kwargs) -> Video:
        return await self._client.get_video(self.id, id, **kwargs)

    async def search(
        self,
        query: str,
        *,
        options: List[str],
        group_by: Optional[str] = None,
        threshold: Optional[str] = None,
        operator: Optional[str] = None,
        conversation_option: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        page_limit: Optional[int] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> SearchResult:
        return await self._client.search(
            self.id,
            query,
            options=options,
            group_by=group_by,
            threshold=threshold,
            operator=operator,
            conversation_option=conversation_option,
            filter=filter,
            page_limit=page_limit,
            sort_option=sort_option,
            **kwargs,
        )

    async def combined_search(
        self,
        query: Dict[str, Any],
        *,
        threshold: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        page_limit: Optional[int] = None,
        **kwargs,
    ) -> SearchResult:
        return await self._client.combined_search(
            query,
            threshold=threshold,
            filter=filter,
            page_limit=page_limit,
            **kwargs,
        )

    async def classify(
        self,
        labels: List[ClassifyLabel],
        *,
        options: List[str],
        threshold: Optional[str] = None,
        include_clips: Optional[bool] = None,
        conversation_option: Optional[str] = None,
        page_limit: Optional[int] = None,
        **kwargs,
    ) -> BulkClassifyResult:
        return await self._client.bulk_classify(
            self.id,
            labels,
            options=options,
            threshold=threshold,
            include_clips=include_clips,
            conversation_option=conversation_option,
            page_limit=page_limit,
            **kwargs,
        )
