from typing import List, Optional, Literal, Union, Dict, Any

from ..resource import APIResource
from .. import models
from ..util import remove_none_values


class Search(APIResource):
    def query(
        self,
        index_id: str,
        query: Union[str, Dict[str, Any]],
        options: List[
            Union[str, Literal["visual", "conversation", "text_in_video", "logo"]]
        ],
        *,
        group_by: Optional[Union[str, Literal["video", "clip"]]] = None,
        threshold: Optional[Union[str, Literal["high", "medium", "low"]]] = None,
        operator: Optional[Union[str, Literal["or", "and"]]] = None,
        conversation_option: Optional[
            Union[str, Literal["semantic", "exact_match"]]
        ] = None,
        filter: Optional[Dict[str, Any]] = None,
        page_limit: Optional[int] = None,
        sort_option: Optional[Union[str, Literal["score", "clip_count"]]] = None,
        **kwargs,
    ) -> models.SearchResult:
        json = {
            "index_id": index_id,
            "query": query,
            "search_options": options,
            "group_by": group_by,
            "threshold": threshold,
            "operator": operator,
            "conversation_option": conversation_option,
            "filter": filter,
            "page_limit": page_limit,
            "sort_option": sort_option,
        }
        res = self._post("search", json=remove_none_values(json), **kwargs)
        return models.SearchResult(self, **res)

    def by_page_token(self, page_token: str, **kwargs) -> models.SearchResult:
        res = self._get(f"search/{page_token}", **kwargs)
        return models.SearchResult(self, **res)

    def combined_query(
        self,
        index_id: str,
        query: Dict[str, Any],
        options: List[
            Union[str, Literal["visual", "conversation", "text_in_video", "logo"]]
        ],
        *,
        conversation_option: Optional[
            Union[str, Literal["semantic", "exact_match"]]
        ] = None,
        filter: Optional[Dict[str, Any]] = None,
        page_limit: Optional[int] = None,
        threshold: Optional[Union[str, Literal["high", "medium", "low"]]] = None,
        **kwargs,
    ) -> models.CombinedSearchResult:
        json = {
            "index_id": index_id,
            "query": query,
            "search_options": options,
            "conversation_option": conversation_option,
            "threshold": threshold,
            "filter": filter,
            "page_limit": page_limit,
        }
        res = self._post("search/combined", json=remove_none_values(json), **kwargs)
        return models.CombinedSearchResult(self, **res)
