from __future__ import annotations

from typing import Optional, Dict, Any, Callable, List, TYPE_CHECKING
from pydantic import PrivateAttr

from ._base import ObjectWithTimestamp, BaseModel, ModelMixin, PageInfo, RootModelList

if TYPE_CHECKING:
    from ..resources import Task as TaskResource


class TaskHLS(BaseModel):
    video_url: Optional[str] = None
    thumbnail_urls: Optional[List[str]] = None
    status: Optional[str] = None
    updated_at: Optional[str] = None


class Task(ObjectWithTimestamp):
    _resource: TaskResource = PrivateAttr()
    index_id: str
    video_id: Optional[str] = None
    status: str
    system_metadata: Dict[str, Any]
    hls: Optional[TaskHLS] = None

    def __init__(self, resource: TaskResource, **data):
        super().__init__(**data)
        self._resource = resource

    # Task related methods

    @property
    def done(self) -> bool:
        return self.status in ("ready", "failed")

    def retrieve(self, **kwargs) -> Task:
        return self._resource.retrieve(self.id, **kwargs)

    def delete(self, **kwargs) -> None:
        return self._resource.delete(self.id, **kwargs)

    def wait_for_done(
        self,
        *,
        sleep_interval: float = 5.0,
        callback: Optional[Callable[[Task], None]] = None,
        **kwargs,
    ) -> Task:
        if sleep_interval <= 0:
            raise ValueError("sleep_interval must be greater than 0")
        while not self.done:
            self._resource._sleep(sleep_interval)
            try:
                task = self.retrieve(**kwargs)
                self.status = task.status
                self.system_metadata = task.system_metadata
            except Exception as e:
                print(f"Retrieving task failed: {e}. Retrying..")
                continue
            if callback is not None:
                callback(self)
        return self


class TaskListWithPagination(ModelMixin, BaseModel):
    _resource: TaskResource = PrivateAttr()
    _origin_params: Dict[str, Any] = PrivateAttr()
    data: RootModelList[Task] = []
    page_info: PageInfo

    def __init__(self, resource: TaskResource, origin_params: Dict[str, Any], **data):
        super().__init__(**data)
        self._resource = resource
        self._origin_params = origin_params

    def __iter__(self):
        return self

    def __next__(self) -> RootModelList[Task]:
        if self.page_info.page >= self.page_info.total_page:
            raise StopIteration
        params = self._origin_params
        params["page"] = self.page_info.page + 1
        res = self._resource.list_pagination(**params)
        self.page_info = res.page_info
        return res.data


class TaskStatus(BaseModel):
    index_id: str
    ready: int
    validating: int
    pending: int
    failed: int
    total_result: int


# Transfer Import


class TransferImportVideo(BaseModel):
    video_id: str
    filename: str


class TransferImportFailedFile(BaseModel):
    filename: str
    error_message: str


class TransferImportResponse(BaseModel):
    videos: List[TransferImportVideo] = []
    failed_files: Optional[List[TransferImportFailedFile]] = None


# Transfer Import Status


class TransferImportStatusVideoInfo(BaseModel):
    video_id: str
    filename: str
    created_at: Optional[str] = None


class TransferImportStatusFailedVideoInfo(BaseModel):
    filename: str
    created_at: Optional[str] = None
    error_message: str


class TransferImportStatusResponse(BaseModel):
    not_imported: List[str] = []
    ready: List[TransferImportStatusVideoInfo] = []
    validating: List[TransferImportStatusVideoInfo] = []
    pending: List[TransferImportStatusVideoInfo] = []
    indexing: List[TransferImportStatusVideoInfo] = []
    failed: List[TransferImportStatusFailedVideoInfo] = []
    queued: List[TransferImportStatusVideoInfo] = []


# Transfer Import Log


class TransferImportLogVideoStatus(BaseModel):
    ready: int
    validating: int
    pending: int
    indexing: int
    failed: int
    queued: int


class TransferImportLogFailedFile(BaseModel):
    filename: str
    error_message: str


class TransferImportLog(BaseModel):
    index_id: str
    index_name: str
    created_at: str
    ended_at: Optional[str] = None
    video_status: TransferImportLogVideoStatus
    failed_files: Optional[List[TransferImportLogFailedFile]] = None
