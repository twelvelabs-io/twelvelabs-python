from typing import List, Optional, Union, Literal

from ..client import TwelveLabs

from ..resource import APIResource
from .. import models
from .. import types
from ..util import remove_none_values
from .video import Video


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
        **kwargs,
    ) -> List[models.Index]:
        params = {
            "_id": id,
            "index_name": name,
            "engine_options": engine_options,
            "engine_family": engine_family,
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
        }
        res = self._get("indexes", params=remove_none_values(params), **kwargs)
        # res["page_info"] # TODO what is the best way to provide this data?
        return [models.Index(self, **index) for index in res["data"]]

    def create(
        self,
        name: str,
        engines: List[types.IndexEngine],
        *,
        # engine_id: str = "marengo2.5", # v1.1
        # options: List[str] = ["visual", "conversation", "text_in_video", "logo"], # v1.1
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
