from typing import List, Optional, Literal, Union, Dict, Any, BinaryIO
from io import BytesIO

from ..resource import APIResource
from .. import models
from ..util import remove_none_values

import json as jsonutil


class Search(APIResource):
    def query(
        self,
        index_id: str,
        options: List[Literal["visual", "audio"]],
        *,
        query_text: str = None,
        query_media_type: Literal["image"] = None,
        query_media_file: Union[str, BinaryIO, None] = None,
        query_media_url: str = None,
        group_by: Optional[Literal["video", "clip"]] = None,
        threshold: Optional[Literal["high", "medium", "low", "none"]] = None,
        operator: Optional[Literal["or", "and"]] = None,
        filter: Optional[Dict[str, Any]] = None,
        page_limit: Optional[int] = None,
        sort_option: Optional[Literal["score", "clip_count"]] = None,
        adjust_confidence_level: Optional[float] = None,
        **kwargs,
    ) -> models.SearchResult:
        if not query_text and not query_media_file and not query_media_url:
            raise ValueError("Either `query_text`, `query_media_file` or `query_media_url` must be provided.")
        
        if filter is not None:
            filter = jsonutil.dumps(filter)
        data = {
            "index_id": index_id,
            "query_text": query_text,
            "query_media_type": query_media_type,
            "query_media_url": query_media_url,
            "search_options": options,
            "group_by": group_by,
            "threshold": threshold,
            "operator": operator,
            "filter": filter,
            "page_limit": page_limit,
            "sort_option": sort_option,
            "adjust_confidence_level": adjust_confidence_level,
        }

        files = {}
        opened_files: List[BinaryIO] = []
        if query_media_file is not None:
            if isinstance(query_media_file, str):
                file = open(query_media_file, "rb")
                opened_files.append(file)
                files["query_media_file"] = file
            else:
                files["query_media_file"] = query_media_file
        if len(files) == 0:
            files["_"] = "" # dummy file to make the form data valid

        try:
            res = self._post(
                "search", data=remove_none_values(data), files=files, **kwargs
            )
            return models.SearchResult(self, **res)
        finally:
            for file in opened_files:
                file.close()

    def by_page_token(self, page_token: str, **kwargs) -> models.SearchResult:
        res = self._get(f"search/{page_token}", **kwargs)
        return models.SearchResult(self, **res)
