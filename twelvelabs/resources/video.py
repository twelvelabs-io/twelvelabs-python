from typing import Optional, Dict, Any, Union, List

from ..models._base import RootModelList
from ..resource import APIResource
from .. import models
from ..util import (
    remove_none_values,
    get_local_params,
    handle_comparison_params,
)


class Video(APIResource):
    def retrieve(
        self,
        index_id: str,
        id: str,
        *,
        embedding_option: Optional[List[str]] = None,
        **kwargs,
    ) -> models.Video:
        params = {
            "embedding_option": embedding_option,
        }
        res = self._get(
            f"indexes/{index_id}/videos/{id}",
            params=remove_none_values(params),
            **kwargs,
        )
        return models.Video(self, index_id, **res)

    def list(
        self,
        index_id: str,
        *,
        filename: Optional[str] = None,
        size: Optional[Union[int, Dict[str, int]]] = None,
        width: Optional[Union[int, Dict[str, int]]] = None,
        height: Optional[Union[int, Dict[str, int]]] = None,
        duration: Optional[Union[int, Dict[str, int]]] = None,
        fps: Optional[Union[int, Dict[str, int]]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> RootModelList[models.Video]:
        params = {
            "filename": filename,
            "size": size,
            "width": width,
            "height": height,
            "duration": duration,
            "fps": fps,
            "user_metadata": user_metadata,
            "created_at": created_at,
            "updated_at": updated_at,
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
        }
        handle_comparison_params(params, "fps", fps)
        handle_comparison_params(params, "width", width)
        handle_comparison_params(params, "height", height)
        handle_comparison_params(params, "size", size)
        handle_comparison_params(params, "duration", duration)
        handle_comparison_params(params, "created_at", created_at)
        handle_comparison_params(params, "updated_at", updated_at)
        res = self._get(
            f"indexes/{index_id}/videos", params=remove_none_values(params), **kwargs
        )
        return RootModelList(
            [models.Video(self, index_id, **video) for video in res["data"]]
        )

    def list_pagination(
        self,
        index_id: str,
        *,
        filename: Optional[str] = None,
        size: Optional[Union[int, Dict[str, int]]] = None,
        width: Optional[Union[int, Dict[str, int]]] = None,
        height: Optional[Union[int, Dict[str, int]]] = None,
        duration: Optional[Union[int, Dict[str, int]]] = None,
        fps: Optional[Union[int, Dict[str, int]]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        page: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_option: Optional[str] = None,
        **kwargs,
    ) -> models.VideoListWithPagination:
        local_params = get_local_params(locals().items())
        params = {
            "filename": filename,
            "size": size,
            "width": width,
            "height": height,
            "duration": duration,
            "fps": fps,
            "user_metadata": user_metadata,
            "created_at": created_at,
            "updated_at": updated_at,
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
        }
        handle_comparison_params(params, "fps", fps)
        handle_comparison_params(params, "width", width)
        handle_comparison_params(params, "height", height)
        handle_comparison_params(params, "size", size)
        handle_comparison_params(params, "duration", duration)
        handle_comparison_params(params, "created_at", created_at)
        handle_comparison_params(params, "updated_at", updated_at)

        res = self._get(
            f"indexes/{index_id}/videos", params=remove_none_values(params), **kwargs
        )

        data = [models.Video(self, index_id, **video) for video in res["data"]]
        page_info = models.PageInfo(**res["page_info"])

        return models.VideoListWithPagination(
            self,
            local_params,
            **{"data": data, "page_info": page_info},
        )

    def update(
        self,
        index_id: str,
        id: str,
        *,
        user_metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        json = {
            "user_metadata": user_metadata,
        }
        self._put(
            f"indexes/{index_id}/videos/{id}", json=remove_none_values(json), **kwargs
        )

    def delete(self, index_id: str, id: str, **kwargs) -> None:
        self._delete(f"indexes/{index_id}/videos/{id}", **kwargs)
