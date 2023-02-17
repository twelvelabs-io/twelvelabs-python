from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, PrivateAttr

from .models import ModelMixin


class SearchResult(ModelMixin, BaseModel):
    _client = PrivateAttr()
    query: Optional[str]
    pool: Dict[str, Any] = Field(alias="search_pool")
    options: Optional[List[str]] = Field(alias="search_options")
    conversation_option: Optional[str]
    data: List[Dict[str, Any]]
    page_info: Dict[str, Any]

    def __init__(self, client, **data):
        super().__init__(**data)
        self._client = client

    def __aiter__(self):
        return self

    async def __anext__(self) -> List[Dict[str, Any]]:
        next_page_token = self.page_info.get("next_page_token")
        if not next_page_token:
            raise StopAsyncIteration

        res = await self._client.get_search_result(next_page_token)
        self.page_info = res.page_info
        return res.data


class CombinedSearchResult(SearchResult):
    async def __anext__(self) -> List[Dict[str, Any]]:
        next_page_token = self.page_info.get("next_page_token")
        if not next_page_token:
            raise StopAsyncIteration

        res = await self._client.get_combined_search_result(next_page_token)
        self.page_info = res.page_info
        return res.data
