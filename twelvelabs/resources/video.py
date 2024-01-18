from typing import Optional, List, Dict, Any

from ..resource import APIResource
from .. import models
from ..util import remove_none_values, get_data_with_default


class Video(APIResource):
    def retrieve(self, index_id: str, id: str, **kwargs) -> models.Video:
        res = self._get(f"indexes/{index_id}/videos/{id}", **kwargs)
        return models.Video(self, index_id, **res)

    def list(
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
    ) -> List[models.Video]:
        params = {
            "_id": id,
            "filename": filename,
            "size": size,
            "width": width,
            "height": height,
            "duration": duration,
            "fps": fps,
            "metadata": metadata,
            "created_at": created_at,
            "updated_at": updated_at,
            "indexed_at": indexed_at,
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
        }
        res = self._get(
            f"indexes/{index_id}/videos", params=remove_none_values(params), **kwargs
        )
        # res["page_info"] # TODO what is the best way to provide this data?
        return [models.Video(self, index_id, **video) for video in res["data"]]

    def update(
        self,
        index_id: str,
        id: str,
        *,
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        json = {
            "video_title": title,
            "metadata": metadata,
        }
        self._put(
            f"indexes/{index_id}/videos/{id}", json=remove_none_values(json), **kwargs
        )

    def delete(self, index_id: str, id: str, **kwargs) -> None:
        self._delete(f"indexes/{index_id}/videos/{id}", **kwargs)

    def transcription(
        self,
        index_id: str,
        id: str,
        *,
        start: Optional[float] = None,
        end: Optional[float] = None,
        **kwargs,
    ) -> List[models.VideoValue]:
        params = {
            "start": start,
            "end": end,
        }
        res = self._get(
            f"indexes/{index_id}/videos/{id}/transcription",
            params=remove_none_values(params),
            **kwargs,
        )
        return [
            models.VideoValue(**value)
            for value in get_data_with_default(res, "data", [])
        ]

    def text_in_video(
        self,
        index_id: str,
        id: str,
        *,
        start: Optional[float] = None,
        end: Optional[float] = None,
        **kwargs,
    ) -> List[models.VideoValue]:
        params = {
            "start": start,
            "end": end,
        }
        res = self._get(
            f"indexes/{index_id}/videos/{id}/text-in-video",
            params=remove_none_values(params),
            **kwargs,
        )
        return [
            models.VideoValue(**value)
            for value in get_data_with_default(res, "data", [])
        ]

    def logo(
        self,
        index_id: str,
        id: str,
        *,
        start: Optional[float] = None,
        end: Optional[float] = None,
        **kwargs,
    ) -> List[models.VideoValue]:
        params = {
            "start": start,
            "end": end,
        }
        res = self._get(
            f"indexes/{index_id}/videos/{id}/logo",
            params=remove_none_values(params),
            **kwargs,
        )
        return [
            models.VideoValue(**value)
            for value in get_data_with_default(res, "data", [])
        ]

    def thumbnail(
        self,
        index_id: str,
        id: str,
        *,
        time: Optional[float] = None,
        **kwargs,
    ) -> str:
        params = {
            "time": time,
        }
        res = self._get(
            f"indexes/{index_id}/videos/{id}/thumbnail",
            params=remove_none_values(params),
            **kwargs,
        )
        return res["thumbnail"]