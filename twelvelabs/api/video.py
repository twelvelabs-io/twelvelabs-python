from typing import Any, Dict, List, Optional, Union

from pydantic import PrivateAttr

from .models import ClassifyLabel, Object


class Video(Object):
    _client = PrivateAttr()
    index_id: str
    indexed_at: Optional[str]
    metadata: Dict[str, Any]

    def __init__(self, client, **data):
        super().__init__(**data)
        self._client = client

    async def update(
        self,
        *,
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Union[str, int, float, bool]]] = None,
        **kwargs,
    ):
        await self._client.update_video(
            self.index_id,
            self.id,
            title=title,
            metadata=metadata,
            **kwargs,
        )

    async def delete(self, **kwargs):
        await self._client.delete_video(self.index_id, self.id, **kwargs)

    async def get_transcription(
        self,
        start: Optional[float] = None,
        end: Optional[float] = None,
        **kwargs,
    ):
        return await self._client.get_video_transcription(
            self.index_id,
            self.id,
            start=start,
            end=end,
            **kwargs,
        )

    async def get_text_in_video(
        self,
        start: Optional[float] = None,
        end: Optional[float] = None,
        **kwargs,
    ):
        return await self._client.get_text_in_video(
            self.index_id,
            self.id,
            start=start,
            end=end,
            **kwargs,
        )

    async def get_thumbnail(
        self,
        time: Optional[float] = None,
        **kwargs,
    ) -> str:
        return await self._client.get_video_thumbnail(
            self.index_id,
            self.id,
            time=time,
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
        **kwargs,
    ) -> List[Dict[str, Any]]:
        return await self._client.classify(
            self.id,
            labels,
            options=options,
            threshold=threshold,
            include_clips=include_clips,
            conversation_option=conversation_option,
            **kwargs,
        )
