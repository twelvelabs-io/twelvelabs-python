from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING, Dict, Any, Union, Literal
from pydantic import Field, PrivateAttr

from ._base import BaseModel, ModelMixin, RootModelList, TokenPageInfo

if TYPE_CHECKING:
    from ..resources import Search as SearchResource


class SearchPool(BaseModel):
    total_count: int
    total_duration: float
    index_id: str


class SearchData(BaseModel):
    score: float
    start: float
    end: float
    video_id: str
    confidence: str
    thumbnail_url: Optional[str] = None
    module_confidence: Optional[Dict[str, Any]] = None


class GroupByVideoSearchData(BaseModel):
    clips: Optional[RootModelList[SearchData]] = None
    id: str


class SearchResult(ModelMixin, BaseModel):
    _resource: SearchResource = PrivateAttr()
    pool: SearchPool = Field(alias="search_pool")
    data: RootModelList[Union[SearchData, GroupByVideoSearchData]]
    page_info: TokenPageInfo

    def __init__(self, resource: SearchResource, **data):
        super().__init__(**data)
        self._resource = resource

    def __iter__(self):
        return self

    def __next__(self) -> RootModelList[Union[SearchData, GroupByVideoSearchData]]:
        next_page_token = self.page_info.next_page_token
        if not next_page_token:
            raise StopIteration

        res = self._resource.by_page_token(next_page_token)
        self.page_info = res.page_info
        return res.data


class CombinedSearchResult(SearchResult):
    def __next__(self) -> RootModelList[SearchData]:
        next_page_token = self.page_info.next_page_token
        if not next_page_token:
            raise StopIteration

        res = self._resource.combined_by_page_token(next_page_token)
        self.page_info = res.page_info
        return res.data
