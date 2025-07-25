from __future__ import annotations
from io import BytesIO
from typing import Optional, Union, BinaryIO, List, Dict, Any, TYPE_CHECKING

from ..models import RootModelList
from ..resource import APIResource
from .. import models
from ..util import remove_none_values, get_local_params, handle_comparison_params

if TYPE_CHECKING:
    from ..client import TwelveLabs


class TaskTransfer(APIResource):
    def import_videos(
        self,
        integration_id: str,
        index_id: str,
        user_metadata: Optional[Dict[str, Any]] = None,
        incremental_import: Optional[bool] = None,
        retry_failed: Optional[bool] = None,
        **kwargs,
    ) -> models.TransferImportResponse:
        json = {
            "index_id": index_id,
            "user_metadata": user_metadata,
            "incremental_import": incremental_import,
            "retry_failed": retry_failed,
        }
        res = self._post(
            f"tasks/transfers/import/{integration_id}", json=json, **kwargs
        )
        return models.TransferImportResponse(**res)

    def import_status(
        self, integration_id: str, index_id: str, **kwargs
    ) -> models.TransferImportStatusResponse:
        params = {"index_id": index_id}
        res = self._get(
            f"tasks/transfers/import/{integration_id}/status", params=params, **kwargs
        )
        return models.TransferImportStatusResponse(**res)

    def import_logs(
        self, integration_id: str, **kwargs
    ) -> RootModelList[models.TransferImportLog]:
        res = self._get(f"tasks/transfers/import/{integration_id}/logs", **kwargs)
        return RootModelList([models.TransferImportLog(**log) for log in res["data"]])


class Task(APIResource):
    transfers: TaskTransfer

    def __init__(self, client: TwelveLabs) -> None:
        super().__init__(client)
        self.transfers = TaskTransfer(client)

    def retrieve(self, id: str, **kwargs) -> models.Task:
        res = self._get(f"tasks/{id}", **kwargs)
        return models.Task(self, **res)

    def list(
        self,
        *,
        index_id: Optional[str] = None,
        filename: Optional[str] = None,
        duration: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> RootModelList[models.Task]:
        params = {
            "index_id": index_id,
            "filename": filename,
            "duration": duration,
            "width": width,
            "height": height,
            "created_at": created_at,
            "updated_at": updated_at,
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
        }
        handle_comparison_params(params, "created_at", created_at)
        handle_comparison_params(params, "updated_at", updated_at)
        res = self._get("tasks", params=remove_none_values(params), **kwargs)
        return RootModelList([models.Task(self, **task) for task in res["data"]])

    def list_pagination(
        self,
        *,
        index_id: Optional[str] = None,
        filename: Optional[str] = None,
        duration: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> models.TaskListWithPagination:
        local_params = get_local_params(locals().items())
        params = {
            "index_id": index_id,
            "filename": filename,
            "duration": duration,
            "width": width,
            "height": height,
            "created_at": created_at,
            "updated_at": updated_at,
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
        }
        handle_comparison_params(params, "created_at", created_at)
        handle_comparison_params(params, "updated_at", updated_at)
        res = self._get("tasks", params=remove_none_values(params), **kwargs)

        data = [models.Task(self, **task) for task in res["data"]]
        page_info = models.PageInfo(**res["page_info"])

        return models.TaskListWithPagination(
            self,
            local_params,
            **{"data": data, "page_info": page_info},
        )

    def create(
        self,
        index_id: str,
        *,
        file: Union[str, BinaryIO, None] = None,
        url: Optional[str] = None,
        transcription_file: Union[str, BinaryIO, None] = None,
        transcription_url: Optional[str] = None,
        enable_video_stream: Optional[bool] = None,
        **kwargs,
    ) -> models.Task:
        if not file and not url:
            raise ValueError("Either file or url must be provided")
        data = {
            "index_id": index_id,
            "video_url": url,
            "transcription_url": transcription_url,
            "enable_video_stream": enable_video_stream,
        }

        files = {}
        opened_files: List[BinaryIO] = []

        if file is not None:
            if isinstance(file, str):
                file = open(file, "rb")
                opened_files.append(file)
            files["video_file"] = file

        if transcription_file is not None:
            if isinstance(transcription_file, str):
                transcription_file = open(transcription_file, "rb")
                opened_files.append(transcription_file)
            files["transcription_file"] = transcription_file
            data["provide_transcription"] = True
        if transcription_url is not None:
            data["provide_transcription"] = True

        if url is not None:
            files["video_url"] = BytesIO(url.encode())
        if transcription_url is not None:
            files["transcription_url"] = BytesIO(transcription_url.encode())

        try:
            res = self._post(
                "tasks", data=remove_none_values(data), files=files, **kwargs
            )
            return self.retrieve(res["_id"])
        finally:
            for file in opened_files:
                file.close()

    def create_bulk(
        self,
        index_id: str,
        *,
        files: Optional[List[Union[str, BinaryIO, None]]] = None,
        urls: Optional[List[str]] = None,
        enable_video_stream: Optional[bool] = None,
        **kwargs,
    ) -> RootModelList[models.Task]:
        if not files and not urls:
            raise ValueError("Either files or urls must be provided")

        tasks = []
        if files:
            for file in files:
                try:
                    task = self.create(
                        index_id,
                        file=file,
                        enable_video_stream=enable_video_stream,
                        **kwargs,
                    )
                    tasks.append(task)
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
                    continue

        if urls:
            for url in urls:
                try:
                    task = self.create(
                        index_id,
                        url=url,
                        enable_video_stream=enable_video_stream,
                        **kwargs,
                    )
                    tasks.append(task)
                except Exception as e:
                    print(f"Error processing url {url}: {e}")
                    continue

        return RootModelList(tasks)

    def delete(self, id: str, **kwargs) -> None:
        self._delete(f"tasks/{id}", **kwargs)

    def status(self, index_id: str, **kwargs) -> models.TaskStatus:
        params = {"index_id": index_id}
        res = self._get("tasks/status", params=params, **kwargs)
        return models.TaskStatus(**res)
