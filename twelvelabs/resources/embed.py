from typing import Union, List, Literal, Optional, Dict, Any

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
        scopes: List[Literal["clip", "video"]],
        *,
        video_url: Optional[str],
        video_start_offset_sec: Optional[float],
        video_end_offset_sec: Optional[float],
        video_clip_length: Optional[int],
        **kwargs,
    ) -> str:
        data = {
            "engine_name": engine_name,
            "video_embedding_scope": scopes,
            "video_url": video_url,
            "video_start_offset_sec": video_start_offset_sec,
            "video_end_offset_sec": video_end_offset_sec,
            "video_clip_length": video_clip_length,
        }
        res = self._post("embed/tasks", data=remove_none_values(data), **kwargs)
        return res["_id"]

    def task_status(self, task_id: str, **kwargs) -> models.EmbeddingsTaskStatus:
        res = self._get(f"embed/tasks/{task_id}/status", **kwargs)
        return models.EmbeddingsTaskStatus(**res)

    def retrieve_task(self, task_id: str, **kwargs) -> models.EmbeddingsTask:
        res = self._get(f"embed/tasks/{task_id}", **kwargs)
        return models.EmbeddingsTask(**res)
