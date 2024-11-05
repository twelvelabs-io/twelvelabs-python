from __future__ import annotations
from io import BytesIO
from typing import Union, List, Literal, Optional, BinaryIO, TYPE_CHECKING

from ..models._base import RootModelList
from ..resource import APIResource
from .. import models
from ..util import remove_none_values, get_local_params


if TYPE_CHECKING:
    from ..client import TwelveLabs


class EmbedTask(APIResource):
    def retrieve(self, id: str, **kwargs) -> models.EmbeddingsTask:
        res = self._get(f"embed/tasks/{id}", **kwargs)
        return models.EmbeddingsTask(self, **res)

    def list(
        self,
        *,
        started_at: Optional[str] = None,
        ended_at: Optional[str] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        status: Optional[Literal["processing", "ready", "failed"]] = None,
        **kwargs,
    ) -> RootModelList[models.EmbeddingsTask]:
        params = {
            "started_at": started_at,
            "ended_at": ended_at,
            "page": page,
            "page_limit": page_limit,
            "status": status,
        }
        res = self._get("embed/tasks", params=remove_none_values(params), **kwargs)
        return RootModelList(
            [models.EmbeddingsTask(self, **task) for task in res["data"]]
        )

    def list_pagination(
        self,
        *,
        started_at: Optional[str] = None,
        ended_at: Optional[str] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        status: Optional[Literal["processing", "ready", "failed"]] = None,
        **kwargs,
    ) -> models.EmbeddingsTaskListWithPagination:
        local_params = get_local_params(locals().items())
        params = {
            "started_at": started_at,
            "ended_at": ended_at,
            "page": page,
            "page_limit": page_limit,
            "status": status,
        }
        res = self._get("embed/tasks", params=remove_none_values(params), **kwargs)

        data = [models.EmbeddingsTask(self, **task) for task in res["data"]]
        page_info = models.PageInfo(**res["page_info"])

        return models.EmbeddingsTaskListWithPagination(
            self,
            local_params,
            **{"data": data, "page_info": page_info},
        )

    def create(
        self,
        engine_name: str,
        *,
        video_file: Union[str, BinaryIO, None] = None,
        video_url: Optional[str] = None,
        video_start_offset_sec: Optional[float] = None,
        video_end_offset_sec: Optional[float] = None,
        video_clip_length: Optional[int] = None,
        video_embedding_scopes: Optional[List[Literal["clip", "video"]]] = None,
        **kwargs,
    ) -> models.EmbeddingsTask:
        if not video_file and not video_url:
            raise ValueError("Either video_file or video_url must be provided")
        data = {
            "engine_name": engine_name,
            "video_embedding_scope": video_embedding_scopes,
            "video_url": video_url,
            "video_start_offset_sec": video_start_offset_sec,
            "video_end_offset_sec": video_end_offset_sec,
            "video_clip_length": video_clip_length,
        }

        files = {}
        opened_files: List[BinaryIO] = []
        if video_file is not None:
            if isinstance(video_file, str):
                video_file = open(video_file, "rb")
                opened_files.append(video_file)
            files["video_file"] = video_file
        if video_url is not None:
            files["video_url"] = BytesIO(video_url.encode())

        try:
            res = self._post(
                "embed/tasks",
                data=remove_none_values(data),
                files=files,
                **kwargs,
            )
            task_id = res["_id"]
            return self.retrieve(task_id)
        finally:
            for file in opened_files:
                file.close()

    def create_bulk(
        self,
        engine_name: str,
        videos: List[models.CreateEmbeddingsTaskVideoParams],
        **kwargs,
    ) -> RootModelList[models.EmbeddingsTask]:
        tasks = []
        for video_params in videos:
            try:
                task = self.create(
                    engine_name,
                    video_file=video_params.file,
                    video_url=video_params.url,
                    video_start_offset_sec=video_params.start_offset_sec,
                    video_end_offset_sec=video_params.end_offset_sec,
                    video_clip_length=video_params.clip_length,
                    scopes=video_params.scopes,
                    **kwargs,
                )
                tasks.append(task)
            except Exception as e:
                print(f"Error creating task with video: {e}")
                continue
        return tasks

    def status(self, task_id: str, **kwargs) -> models.EmbeddingsTaskStatus:
        res = self._get(f"embed/tasks/{task_id}/status", **kwargs)
        return models.EmbeddingsTaskStatus(**res)


class Embed(APIResource):
    task: EmbedTask

    def __init__(self, client: TwelveLabs) -> None:
        super().__init__(client)
        self.task = EmbedTask(client)

    def create(
        self,
        engine_name: str,
        *,
        # text params
        text: str = None,
        text_truncate: Literal["none", "start", "end"] = None,
        # audio params
        audio_url: str = None,
        audio_file: Union[str, BinaryIO, None] = None,
        audio_start_offset_sec: Optional[float] = None,
        # image params
        image_url: str = None,
        image_file: Union[str, BinaryIO, None] = None,
        **kwargs,
    ) -> models.CreateEmbeddingsResult:
        if not any([text, audio_url, audio_file, image_url, image_file]):
            raise ValueError(
                "At least one of text, audio_url, audio_file, image_url, image_file must be provided"
            )
        data = {
            "engine_name": engine_name,
            "text": text,
            "text_truncate": text_truncate,
            "audio_url": audio_url,
            "audio_start_offset_sec": audio_start_offset_sec,
            "image_url": image_url,
        }
        files = {}
        opened_files: List[BinaryIO] = []

        if text is not None:
            files["text"] = BytesIO(text.encode())
        if audio_url is not None:
            files["audio_url"] = BytesIO(audio_url.encode())
        if image_url is not None:
            files["image_url"] = BytesIO(image_url.encode())

        if audio_file is not None:
            if isinstance(audio_file, str):
                audio_file = open(audio_file, "rb")
                opened_files.append(audio_file)
            files["audio_file"] = audio_file
        if image_file is not None:
            if isinstance(image_file, str):
                image_file = open(image_file, "rb")
                opened_files.append(image_file)
            files["image_file"] = image_file

        try:
            res = self._post(
                "embed",
                data=remove_none_values(data),
                files=files,
                **kwargs,
            )
            return models.CreateEmbeddingsResult(**res)
        finally:
            for file in opened_files:
                file.close()
