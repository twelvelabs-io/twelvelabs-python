from typing import Union, List, Literal, Optional, Dict, Any

from ..resource import APIResource
from .. import models
from ..util import remove_none_values


class Classify(APIResource):
    def videos(
        self,
        video_ids: List[str],
        options: List[Union[str, Literal["visual", "conversation", "text_in_video"]]],
        classes: List[models.ClassifyClassParams],
        *,
        conversation_option: Optional[
            Union[str, Literal["semantic", "exact_match"]]
        ] = "semantic",
        page_limit: Optional[int] = None,
        include_clips: Optional[bool] = None,
        threshold: Optional[Dict[str, Any]] = None,
        show_detailed_score: Optional[bool] = None,
        **kwargs,
    ) -> models.ClassifyPageResult:
        json = {
            "video_ids": video_ids,
            "options": options,
            "classes": classes,
            "conversation_option": conversation_option,
            "page_limit": page_limit,
            "include_clips": include_clips,
            "threshold": threshold,
            "show_detailed_score": show_detailed_score,
        }
        res = self._post("classify", json=remove_none_values(json), **kwargs)
        return models.ClassifyPageResult(self, **res)

    def index(
        self,
        index_id: str,
        options: List[Union[str, Literal["visual", "conversation", "text_in_video"]]],
        classes: List[models.ClassifyClassParams],
        *,
        conversation_option: Optional[
            Union[str, Literal["semantic", "exact_match"]]
        ] = "semantic",
        page_limit: Optional[int] = None,
        include_clips: Optional[bool] = None,
        threshold: Optional[Dict[str, Any]] = None,
        show_detailed_score: Optional[bool] = None,
        **kwargs,
    ) -> models.ClassifyPageResult:
        json = {
            "index_id": index_id,
            "options": options,
            "classes": classes,
            "conversation_option": conversation_option,
            "page_limit": page_limit,
            "include_clips": include_clips,
            "threshold": threshold,
            "show_detailed_score": show_detailed_score,
        }
        res = self._post("classify/bulk", json=remove_none_values(json), **kwargs)
        return models.ClassifyPageResult(self, **res)

    def by_page_token(
        self,
        page_token: str,
        **kwargs,
    ) -> models.ClassifyPageResult:
        res = self._get(f"classify/{page_token}", **kwargs)
        return models.ClassifyPageResult(self, **res)
