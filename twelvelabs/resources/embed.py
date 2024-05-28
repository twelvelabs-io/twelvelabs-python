from typing import Union, List, Literal, Optional, BinaryIO

from ..resource import APIResource
from .. import models
from ..util import remove_none_values


class Embed(APIResource):
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

    def create_task(
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

        try:
            res = self._post(
                "embed/tasks", data=remove_none_values(data), files={files}, **kwargs
            )
            return res["_id"]
        finally:
            for file in opened_files:
                file.close()

    def task_status(self, task_id: str, **kwargs) -> models.EmbeddingsTaskStatus:
        res = self._get(f"embed/tasks/{task_id}/status", **kwargs)
        return models.EmbeddingsTaskStatus(**res)

    def retrieve_task(self, task_id: str, **kwargs) -> models.EmbeddingsTask:
        res = self._get(f"embed/tasks/{task_id}", **kwargs)
        return models.EmbeddingsTask(**res)
