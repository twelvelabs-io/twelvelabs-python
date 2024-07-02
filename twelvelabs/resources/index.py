from __future__ import annotations
from typing import (
    List,
    Optional,
    Union,
    Literal,
    Dict,
    TYPE_CHECKING,
)

from ..models import RootModelList
from ..resource import APIResource
from .. import models
from .. import types
from ..util import remove_none_values, get_local_params, handle_comparison_params
from .video import Video

if TYPE_CHECKING:
    from ..client import TwelveLabs


class Index(APIResource):
    video: Video

    def __init__(self, client: TwelveLabs) -> None:
        super().__init__(client)
        self.video = Video(client)

    def retrieve(self, id: str, **kwargs) -> models.Index:
        res = self._get(f"indexes/{id}", **kwargs)
        return models.Index(self, **res)

    def list(
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        engine_options: Optional[
            List[Union[str, Literal["visual", "conversation", "text_in_video", "logo"]]]
        ] = None,
        engine_family: Optional[Union[str, Literal["marengo", "pegasus"]]] = None,
        page: Optional[int] = 1,
        page_limit: Optional[int] = 10,
        sort_by: Optional[str] = "created_at",
        sort_option: Optional[str] = "desc",
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        **kwargs,
    ) -> RootModelList[models.Index]:
        params = {
            "_id": id,
            "index_name": name,
            "engine_options": engine_options,
            "engine_family": engine_family,
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        handle_comparison_params(params, "created_at", created_at)
        handle_comparison_params(params, "updated_at", updated_at)
        res = self._get("indexes", params=remove_none_values(params), **kwargs)

        return RootModelList([models.Index(self, **index) for index in res["data"]])

    def list_pagination(
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        engine_options: Optional[
            List[Union[str, Literal["visual", "conversation", "text_in_video", "logo"]]]
        ] = None,
        engine_family: Optional[Union[str, Literal["marengo", "pegasus"]]] = None,
        page: Optional[int] = 1,
        page_limit: Optional[int] = 10,
        sort_by: Optional[str] = "created_at",
        sort_option: Optional[str] = "desc",
        created_at: Optional[Union[str, Dict[str, str]]] = None,
        updated_at: Optional[Union[str, Dict[str, str]]] = None,
        **kwargs,
    ) -> models.IndexListWithPagination:
        local_params = get_local_params(locals().items())
        params = {
            "_id": id,
            "index_name": name,
            "engine_options": engine_options,
            "engine_family": engine_family,
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        handle_comparison_params(params, "created_at", created_at)
        handle_comparison_params(params, "updated_at", updated_at)

        res = self._get("indexes", params=remove_none_values(params), **kwargs)

        data = [models.Index(self, **index) for index in res["data"]]
        page_info = models.PageInfo(**res["page_info"])

        return models.IndexListWithPagination(
            self,
            local_params,
            **{"data": data, "page_info": page_info},
        )

    def create(
        self,
        name: str,
        engines: List[types.IndexEngine],
        *,
        addons: Optional[List[str]] = None,
        **kwargs,
    ) -> models.Index:
        json = {
            "index_name": name,
            "engines": list(
                map(
                    lambda engine: {
                        "engine_name": engine["name"],
                        "engine_options": engine["options"],
                    },
                    engines,
                )
            ),
            "addons": addons,
        }
        resp = self._post("indexes", json=json, **kwargs)
        return self.retrieve(resp["_id"])

    def update(self, id: str, name: str, **kwargs) -> None:
        json = {"index_name": name}
        self._put(f"indexes/{id}", json=json, **kwargs)

    def delete(self, id: str, **kwargs) -> None:
        self._delete(f"indexes/{id}", **kwargs)
