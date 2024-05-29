from __future__ import annotations
from typing import Union, List, Literal, Optional, BinaryIO, TYPE_CHECKING

from ..resource import APIResource
from .. import models
from ..util import remove_none_values


if TYPE_CHECKING:
    from ..client import TwelveLabs


class EmbedTask(APIResource):
    def retrieve(self, id: str, **kwargs) -> models.EmbeddingsTask:
        res = self._get(f"embed/tasks/{id}", **kwargs)
        return models.EmbeddingsTask(**res)

    def create(
        self,
        engine_name: str,
        *,
        video_file: Union[str, BinaryIO, None] = None,
        video_url: Optional[str] = None,
        video_start_offset_sec: Optional[float] = None,
        video_end_offset_sec: Optional[float] = None,
        video_clip_length: Optional[int] = None,
        scopes: Optional[List[Literal["clip", "video"]]] = None,
        **kwargs,
    ) -> str:
        if not video_file and not video_url:
            raise ValueError("Either video_file or video_url must be provided")
        data = {
            "engine_name": engine_name,
            "video_embedding_scope": scopes,
            "video_url": video_url,
            "video_start_offset_sec": video_start_offset_sec,
            "video_end_offset_sec": video_end_offset_sec,
            "video_clip_length": video_clip_length,
        }

        files = {}
        opened_files: List[BinaryIO] = []
        if video_file is not None:
            if isinstance(video_file, str):
                file = open(video_file, "rb")
                opened_files.append(file)
                files["video_file"] = file
            else:
                files["video_file"] = video_file

        try:
            res = self._post(
                "embed/tasks", data=remove_none_values(data), files=files, **kwargs
            )
            return res["_id"]
        finally:
            for file in opened_files:
                file.close()

    def create_bulk(
        self,
        engine_name: str,
        videos: models.CreateEmbeddingsTaskVideoParams,
        **kwargs,
    ) -> List[str]:
        task_ids = []
        for video_params in videos:
            try:
                task_id = self.create(
                    engine_name,
                    video_file=video_params.file,
                    video_url=video_params.url,
                    video_start_offset_sec=video_params.start_offset_sec,
                    video_end_offset_sec=video_params.end_offset_sec,
                    video_clip_length=video_params.clip_length,
                    scopes=video_params.scopes,
                    **kwargs,
                )
                task_ids.append(task_id)
            except Exception as e:
                print(f"Error creating task with video: {e}")
                continue
        return task_ids

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
        text: str,
        text_truncate: Literal["none", "start", "end"],
        **kwargs,
    ) -> models.CreateEmbeddingsResult:
        data = {
            "engine_name": engine_name,
            "text": text,
            "text_truncate": text_truncate,
        }
        res = self._post("embed", data=remove_none_values(data), **kwargs)
        return models.CreateEmbeddingsResult(**res)
