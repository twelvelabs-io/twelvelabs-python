from typing import Any, Dict, List

from pydantic import BaseModel, PrivateAttr

from .models import ModelMixin


class BulkClassifyResult(ModelMixin, BaseModel):
    _client = PrivateAttr()
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

        res = await self._client.get_bulk_classify_result(next_page_token)
        self.page_info = res.page_info
        return res.data
