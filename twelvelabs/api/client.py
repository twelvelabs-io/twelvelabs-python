import asyncio
from typing import Any, BinaryIO, Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin

import aiohttp

from .classify import BulkClassifyResult
from .errors import APIError
from .index import Index
from .models import ClassifyLabel, Engine, VideoFile
from .search import CombinedSearchResult, SearchResult
from .task import Task
from .video import Video

BASE_URL = "https://api.twelvelabs.io"
API_KEY_HEADER_NAME = "x-api-key"


class APIClient:
    def __init__(self, api_key: str, version: str = "v1.1"):
        self.api_key = api_key
        self.version = version
        self._base_url = f"{BASE_URL}/{self.version}/"
        self._session = aiohttp.ClientSession(
            headers={
                API_KEY_HEADER_NAME: self.api_key,
            },
            cookie_jar=aiohttp.DummyCookieJar(),
        )

    async def request(self, method: str, path: str, **kwargs) -> Any:
        url = urljoin(self._base_url, path)
        async with self._session.request(method, url, **kwargs) as resp:
            if not (200 <= resp.status < 300):
                data = await resp.json(content_type=None)
                # Response body can be a JSON string, which indicates that there was
                # an internal server error.
                # In this case, just call raise_for_status() to throw the default
                # exception.
                if not isinstance(data, dict):
                    resp.raise_for_status()
                raise APIError(data["message"], data.get("code"), data.get("docs_url"))
            return await resp.json(content_type=None)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._session.close()

    async def get_engines(self, **kwargs) -> List[Engine]:
        resp = await self.request("GET", "engines", **kwargs)
        return [Engine(**engine) for engine in resp["data"]]

    async def get_engine(self, id: str, **kwargs) -> Engine:
        resp = await self.request("GET", f"engines/{id}", **kwargs)
        return Engine(**resp)

    async def create_index(
        self,
        name: str,
        *,
        engine_id: str = "marengo2",
        options: List[str] = ["visual", "conversation", "text_in_video", "logo"],
        addons: Optional[List[str]] = ["thumbnail"],
        **kwargs,
    ) -> Index:
        json = {
            "index_name": name,
            "engine_id": engine_id,
            "index_options": options,
        }
        if addons is not None:
            json["addons"] = addons
        resp = await self.request("POST", "indexes", json=json, **kwargs)
        return await self.get_index(resp["_id"])

    async def list_indexes(
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        options: Optional[str] = None,  # TODO: List[str]?
        page: Optional[int] = 1,
        page_limit: Optional[int] = 10,
        sort_by: Optional[str] = "created_at",
        sort_option: Optional[str] = "desc",
        **kwargs,
    ) -> Tuple[List[Index], int, int]:
        params: Dict[str, Any] = {}
        if id is not None:
            params["_id"] = id
        if name is not None:
            params["index_name"] = name
        if options is not None:
            params["index_options"] = options
        if page is not None:
            params["page"] = page
        if page_limit is not None:
            params["page_limit"] = page_limit
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_option is not None:
            params["sort_option"] = sort_option
        resp = await self.request("GET", "indexes", params=params, **kwargs)
        page_info = resp["page_info"]
        return (
            [Index(self, **index) for index in resp["data"]],
            page_info["total_page"],
            page_info["total_results"],
        )

    async def get_indexes(
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        options: Optional[str] = None,  # TODO: List[str]?
        page: Optional[int] = 1,
        page_limit: Optional[int] = 10,
        sort_by: Optional[str] = "created_at",
        sort_option: Optional[str] = "desc",
        **kwargs,
    ) -> List[Index]:
        indexes, *_ = await self.list_indexes(
            id=id,
            name=name,
            options=options,
            page=page,
            page_limit=page_limit,
            sort_by=sort_by,
            sort_option=sort_option,
            **kwargs,
        )
        return indexes

    async def get_index(self, id: str, **kwargs) -> Index:
        resp = await self.request("GET", f"indexes/{id}", **kwargs)
        return Index(self, **resp)

    async def update_index(self, id: str, *, name: str, **kwargs):
        json = {"index_name": name}
        await self.request("put", f"indexes/{id}", json=json, **kwargs)

    async def delete_index(self, id: str, **kwargs):
        await self.request("DELETE", f"indexes/{id}", **kwargs)

    async def upload_video(
        self,
        index_id: str,
        *,
        file: Union[str, BinaryIO, None] = None,
        url: Optional[str] = None,
        transcription_file: Union[str, BinaryIO, None] = None,
        transcription_url: Optional[str] = None,
        language: Optional[str] = None,
        **kwargs,
    ) -> Task:
        if not file and not url:
            raise ValueError("Either file or url must be provided")
        data: Dict[str, Any] = {"index_id": index_id}
        opened_files: List[BinaryIO] = []
        if file is not None:
            if isinstance(file, str):
                file = open(file, "rb")
                opened_files.append(file)
            data["video_file"] = file
        if transcription_file is not None:
            if isinstance(transcription_file, str):
                transcription_file = open(transcription_file, "rb")
                opened_files.append(transcription_file)
            data["transcription_file"] = transcription_file
            data["provide_transcription"] = True
        if url is not None:
            data["video_url"] = url
        if transcription_url is not None:
            data["transcription_url"] = transcription_url
            data["provide_transcription"] = True
        if language is not None:
            data["language"] = language
        try:
            resp = await self.request("POST", "tasks", data=data, **kwargs)
            return await self.get_task(resp["_id"])
        finally:
            for file in opened_files:
                file.close()

    async def upload_videos(
        self, index_id: str, videos: List[VideoFile], **kwargs
    ) -> List[Task]:
        return await asyncio.gather(
            *[self.upload_video(index_id, **video, **kwargs) for video in videos]
        )

    async def list_tasks(
        self,
        *,
        id: Optional[str] = None,
        index_id: Optional[str] = None,
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
        params: Dict[str, Any] = {}
        if id is not None:
            params["_id"] = id
        if index_id is not None:
            params["index_id"] = index_id
        if filename is not None:
            params["filename"] = filename
        if duration is not None:
            params["duration"] = duration
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if created_at is not None:
            params["created_at"] = created_at
        if updated_at is not None:
            params["updated_at"] = updated_at
        if estimated_time is not None:
            params["estimated_time"] = estimated_time
        if page is not None:
            params["page"] = page
        if page_limit is not None:
            params["page_limit"] = page_limit
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_option is not None:
            params["sort_option"] = sort_option
        resp = await self.request("GET", "tasks", params=params, **kwargs)
        page_info = resp["page_info"]
        print(resp)
        return (
            [Task(self, **task) for task in resp["data"]],
            page_info["total_page"],
            page_info["total_results"],
        )

    async def get_tasks(
        self,
        *,
        id: Optional[str] = None,
        index_id: Optional[str] = None,
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
        tasks, *_ = await self.list_tasks(
            id=id,
            index_id=index_id,
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
        return tasks

    async def get_task(self, id: str, **kwargs) -> Task:
        resp = await self.request("GET", f"tasks/{id}", **kwargs)
        return Task(self, **resp)

    async def delete_task(self, id: str, **kwargs):
        await self.request("DELETE", f"tasks/{id}", **kwargs)

    async def tasks_status(self, index_id: str, **kwargs) -> Dict[str, Any]:
        params = {"index_id": index_id}
        resp = await self.request("GET", "tasks/status", params=params, **kwargs)
        return resp

    async def cloud_to_cloud_transfer(self, file: BinaryIO, **kwargs):
        files = {"file": file}
        await self.request("POST", "tasks/transfers", files=files, **kwargs)

    async def list_videos(
        self,
        index_id: str,
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
        params: Dict[str, Any] = {}
        if id is not None:
            params["_id"] = id
        if filename is not None:
            params["filename"] = filename
        if size is not None:
            params["size"] = size
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        if duration is not None:
            params["duration"] = duration
        if fps is not None:
            params["fps"] = fps
        if metadata is not None:
            params["metadata"] = metadata
        if created_at is not None:
            params["created_at"] = created_at
        if updated_at is not None:
            params["updated_at"] = updated_at
        if indexed_at is not None:
            params["indexed_at"] = indexed_at
        if page is not None:
            params["page"] = page
        if page_limit is not None:
            params["page_limit"] = page_limit
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_option is not None:
            params["sort_option"] = sort_option
        resp = await self.request(
            "GET", f"indexes/{index_id}/videos", params=params, **kwargs
        )
        page_info = resp["page_info"]
        return (
            [Video(self, index_id=index_id, **video) for video in resp["data"]],
            page_info["total_page"],
            page_info["total_results"],
        )

    async def get_videos(
        self,
        index_id: str,
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
        videos, *_ = await self.list_videos(
            index_id,
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
        return videos

    async def get_video(self, index_id: str, id: str, **kwargs) -> Video:
        resp = await self.request("GET", f"indexes/{index_id}/videos/{id}", **kwargs)
        return Video(self, index_id=index_id, **resp)

    async def update_video(
        self,
        index_id: str,
        id: str,
        *,
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Union[str, int, float, bool]]] = None,
        **kwargs,
    ):
        json: Dict[str, Any] = {}
        if title is not None:
            json["video_title"] = title
        if metadata is not None:
            json["metadata"] = metadata
        await self.request(
            "PUT", f"indexes/{index_id}/videos/{id}", json=json, **kwargs
        )

    async def delete_video(self, index_id: str, id: str, **kwargs):
        await self.request("DELETE", f"indexes/{index_id}/videos{id}", **kwargs)

    async def get_video_transcription(
        self,
        index_id: str,
        video_id: str,
        *,
        start: Optional[float] = None,
        end: Optional[float] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        resp = await self.request(
            "GET",
            f"indexes/{index_id}/videos/{video_id}/transcription",
            params=params,
            **kwargs,
        )
        return resp["data"]

    async def get_text_in_video(
        self,
        index_id: str,
        video_id: str,
        *,
        start: Optional[float] = None,
        end: Optional[float] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        resp = await self.request(
            "GET",
            f"indexes/{index_id}/videos/{video_id}/text-in-video",
            params=params,
            **kwargs,
        )
        return resp["data"]

    async def get_video_thumbnail(
        self,
        index_id: str,
        video_id: str,
        *,
        time: Optional[float] = None,
        **kwargs,
    ) -> str:
        params = {}
        if time is not None:
            params["time"] = time
        resp = await self.request(
            "GET",
            f"indexes/{index_id}/videos/{video_id}/thumbnail",
            params=params,
            **kwargs,
        )
        return resp["thumbnail"]

    async def search(
        self,
        index_id: str,
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
        json: Dict[str, Any] = {
            "index_id": index_id,
            "query": query,
            "search_options": options,
        }
        if group_by is not None:
            json["group_by"] = group_by
        if threshold is not None:
            json["threshold"] = threshold
        if sort_option is not None:
            json["sort_option"] = sort_option
        if operator is not None:
            json["operator"] = operator
        if conversation_option is not None:
            json["conversation_option"] = conversation_option
        if page_limit is not None:
            json["page_limit"] = page_limit
        if filter is not None:
            json["filter"] = filter
        resp = await self.request("POST", "search", json=json, **kwargs)
        return SearchResult(self, **resp)

    async def get_search_result(self, page_token: str, **kwargs) -> SearchResult:
        resp = await self.request("GET", f"search/{page_token}", **kwargs)
        return SearchResult(self, **resp)

    async def combined_search(
        self,
        index_id: str,
        query: Dict[str, Any],
        *,
        threshold: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        page_limit: Optional[int] = None,
        **kwargs,
    ) -> CombinedSearchResult:
        json: Dict[str, Any] = {
            "index_id": index_id,
            "query": query,
        }
        if threshold is not None:
            json["threshold"] = threshold
        if page_limit is not None:
            json["page_limit"] = page_limit
        if filter is not None:
            json["filter"] = filter
        resp = await self.request("POST", "beta/search", json=json, **kwargs)
        return CombinedSearchResult(self, **resp)

    async def get_combined_search_result(
        self, page_token: str, **kwargs
    ) -> CombinedSearchResult:
        resp = await self.request("GET", f"beta/search/{page_token}", **kwargs)
        return CombinedSearchResult(self, **resp)

    async def classify(
        self,
        video_id: str,
        labels: List[ClassifyLabel],
        *,
        options: List[str],
        threshold: Optional[str] = None,
        include_clips: Optional[bool] = None,
        conversation_option: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        json: Dict[str, Any] = {
            "labels": labels,
            "video_id": video_id,
            "options": options,
        }
        if threshold is not None:
            json["threshold"] = threshold
        if include_clips is not None:
            json["include_clips"] = include_clips
        if conversation_option is not None:
            json["conversation_option"] = conversation_option
        resp = await self.request("POST", "classify", json=json, **kwargs)
        return resp["labels"]

    async def bulk_classify(
        self,
        index_id: str,
        labels: List[ClassifyLabel],
        *,
        options: List[str],
        threshold: Optional[str] = None,
        include_clips: Optional[bool] = None,
        conversation_option: Optional[str] = None,
        page_limit: Optional[int] = None,
        **kwargs,
    ) -> BulkClassifyResult:
        json: Dict[str, Any] = {
            "labels": labels,
            "index_id": index_id,
            "options": options,
        }
        if threshold is not None:
            json["threshold"] = threshold
        if include_clips is not None:
            json["include_clips"] = include_clips
        if conversation_option is not None:
            json["conversation_option"] = conversation_option
        if page_limit is not None:
            json["page_limit"] = page_limit
        resp = await self.request("POST", "classify/bulk", json=json, **kwargs)
        return BulkClassifyResult(self, **resp)

    async def get_bulk_classify_result(
        self,
        page_token: str,
        **kwargs,
    ) -> BulkClassifyResult:
        resp = await self.request("GET", f"classify/{page_token}", **kwargs)
        return BulkClassifyResult(self, **resp)
