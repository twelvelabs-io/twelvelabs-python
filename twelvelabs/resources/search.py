from typing import List, Optional, Literal, Union, Dict, Any, BinaryIO

from ..resource import APIResource
from .. import models
from ..util import remove_none_values

import json as jsonutil


class Search(APIResource):
    def query(
        self,
        index_id: str,
        options: List[
            Literal["visual", "conversation", "text_in_video", "logo", "face"]
        ],
        *,
        query: Union[str, Dict[str, Any]] = None,  # deprecated
        query_text: str = None,
        query_image_file: Union[str, BinaryIO, None] = None,
        query_image_url: str = None,
        group_by: Optional[Literal["video", "clip"]] = None,
        threshold: Optional[Literal["high", "medium", "low", "none"]] = None,
        operator: Optional[Literal["or", "and"]] = None,
        conversation_option: Optional[Literal["semantic", "exact_match"]] = None,
        filter: Optional[Dict[str, Any]] = None,
        page_limit: Optional[int] = None,
        sort_option: Optional[Literal["score", "clip_count"]] = None,
        adjust_confidence_level: Optional[float] = None,
        **kwargs,
    ) -> models.SearchResult:
        if not query_text and not query_image_file and not query_image_url:
            if query is not None:
                # deprecated; call /search endpoint
                print(
                    "Warning: `query` is deprecated. Use `query_text` or `query_image_file` or `query_image_url` instead."
                )
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
            else:
                raise ValueError(
                    "Either query_text, query_image_file, or query_image_url must be provided"
                )
        if filter is not None:
            filter = jsonutil.dumps(filter)
        data = {
            "index_id": index_id,
            "query_text": query_text,
            "query_image_url": query_image_url,
            "search_options": options,
            "group_by": group_by,
            "threshold": threshold,
            "operator": operator,
            "conversation_option": conversation_option,
            "filter": filter,
            "page_limit": page_limit,
            "sort_option": sort_option,
            "adjust_confidence_level": adjust_confidence_level,
        }

        files = {}
        opened_files: List[BinaryIO] = []
        if query_image_file is not None:
            data["query_media_type"] = "image"
            if isinstance(query_image_file, str):
                file = open(query_image_file, "rb")
                opened_files.append(file)
                files["query_media_file"] = file
            else:
                files["query_media_file"] = query_image_file
        else:
            # Request should be sent as multipart-form even file not exists
            files["dummy"] = ("", "")

        try:
            res = self._post(
                "search-v2", data=remove_none_values(data), files=files, **kwargs
            )
            return models.SearchResult(self, **res)
        finally:
            for file in opened_files:
                file.close()

    def by_page_token(self, page_token: str, **kwargs) -> models.SearchResult:
        res = self._get(f"search-v2/{page_token}", **kwargs)
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
