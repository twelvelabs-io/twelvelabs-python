import typing
from ..core.client_wrapper import SyncClientWrapper
from ..search.client import SearchClient
from ..types.search_item import SearchItem
from ..core.pagination import SyncPager, AsyncPager
from ..core.client_wrapper import AsyncClientWrapper
from ..core.pydantic_utilities import parse_obj_as
from ..search.client import AsyncSearchClient
from ..search.types.search_create_request_search_options_item import (
    SearchCreateRequestSearchOptionsItem,
)
from ..search.types.search_create_request_group_by import SearchCreateRequestGroupBy
from ..types.threshold_search import ThresholdSearch
from ..search.types.search_create_request_sort_option import (
    SearchCreateRequestSortOption,
)
from ..search.types.search_create_request_operator import SearchCreateRequestOperator
from ..types.search_results import SearchResults
from ..core.request_options import RequestOptions
from .. import core

OMIT = typing.cast(typing.Any, ...)


class SearchClientWrapper(SearchClient):
    def __init__(self, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def _get_next_page(self, page_token: str) -> SyncPager[SearchItem]:
        _response = self._raw_client._client_wrapper.httpx_client.request(
            f"search/{page_token}",
            method="GET",
        )
        _parsed_response = typing.cast(
            SearchResults,
            parse_obj_as(
                type_=SearchResults,
                object_=_response.json(),
            ),
        )
        _has_next = (
            _parsed_response.page_info is not None
            and _parsed_response.page_info.next_page_token is not None
        )
        _get_next = lambda: self._get_next_page(
            _parsed_response.page_info.next_page_token  # type: ignore
        )
        _items = _parsed_response.data
        return SyncPager(
            has_next=_has_next, items=_items, get_next=_get_next, response=None
        )

    def query(
        self,
        *,
        index_id: str,
        search_options: typing.List[SearchCreateRequestSearchOptionsItem],
        query_media_type: typing.Optional[typing.Literal["image"]] = OMIT,
        query_media_url: typing.Optional[str] = OMIT,
        query_media_file: typing.Optional[core.File] = OMIT,
        query_text: typing.Optional[str] = OMIT,
        adjust_confidence_level: typing.Optional[float] = OMIT,
        group_by: typing.Optional[SearchCreateRequestGroupBy] = OMIT,
        threshold: typing.Optional[ThresholdSearch] = OMIT,
        sort_option: typing.Optional[SearchCreateRequestSortOption] = OMIT,
        operator: typing.Optional[SearchCreateRequestOperator] = OMIT,
        page_limit: typing.Optional[int] = OMIT,
        filter: typing.Optional[str] = OMIT,
        include_user_metadata: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SyncPager[SearchItem]:
        """
        Use this endpoint to search for relevant matches in an index using text or various media queries.
        
        **Text queries**:
        - Use the `query_text` parameter to specify your query.
        
        **Media queries**:
        - Set the `query_media_type` parameter to the corresponding media type (example: `image`).
        - Specify either one of the following parameters:
          - `query_media_url`: Publicly accessible URL of your media file.
          - `query_media_file`: Local media file.
          If both `query_media_url` and `query_media_file` are specified in the same request, `query_media_url` takes precedence.
        <Accordion title="Image requirements">
        Your images must meet the following requirements:
          - **Format**: JPEG and PNG.
          - **Dimension**: Must be at least 64 x 64 pixels.
          - **Size**: Must not exceed 5MB.
          - **Object visibility**: Ensure that the objects of interest are visible and occupy at least 50% of the video frame. This helps the platform accurately identify and match the objects.
        </Accordion>
        
        <Note title="Note">
        This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
        </Note>
        
        Parameters
        ----------
        index_id : str
            The unique identifier of the index to search.
        
        search_options : typing.List[SearchCreateRequestSearchOptionsItem]
            Specifies the [sources of information](/v1.3/docs/concepts/modalities#search-options) the platform uses when performing a search. You must include the `search_options` parameter separately for each desired source of information.
            
            <Note title="Notes">
            - The search options you specify must be a subset of the [model options](/v1.3/docs/concepts/modalities#model-options) used when you created the index.
            - You can specify multiple search options in conjunction with the `operator` parameter described below to broaden or narrow your search.
            
            Example:
            To search using both visual and audio cues, include this parameter twice in the request as shown below:
            ```JSON
            --form search_options=visual \
            --form search_options=audio \
            ```
            </Note>
        
        query_media_type : typing.Optional[typing.Literal["image"]]
            The type of media you wish to use. This parameter is required for media queries. For example, to perform an image-based search, set this parameter to `image`.
        
        query_media_url : typing.Optional[str]
            The publicly accessible URL of the media file you wish to use. This parameter is required for media queries if `query_media_file` is not provided.
        
        query_media_file : typing.Optional[core.File]
            See core.File for more documentation
        
        query_text : typing.Optional[str]
            The text query to search for. This parameter is required for text queries. Note that the platform supports full natural language-based search.
        
        adjust_confidence_level : typing.Optional[float]
            This parameter specifies the strictness of the thresholds for assigning the high, medium, or low confidence levels to search results. If you use a lower value, the thresholds become more relaxed, and more search results will be classified as having high, medium, or low confidence levels. You can use this parameter to include a broader range of potentially relevant video clips, even if some results might be less precise.
            
            **Min**: 0
            **Max**: 1
            **Default:** 0.5
        
        group_by : typing.Optional[SearchCreateRequestGroupBy]
            Use this parameter to group or ungroup items in a response. It can take one of the following values:
            - `video`:  The platform will group the matching video clips in the response by video.
            - `clip`: The matching video clips in the response will not be grouped.
            
            **Default:** `clip`
        
        threshold : typing.Optional[ThresholdSearch]
        
        sort_option : typing.Optional[SearchCreateRequestSortOption]
            Use this parameter to specify the sort order for the response.
            
            When performing a search, the platform determines the level of confidence that each video clip matches your search terms. By default, the search results are sorted on the level of confidence in descending order.
            
            If you set this parameter to `score` and `group_by` is set to `video`, the platform will determine the maximum value of the `score` field for each video and sort the videos in the response by the maximum value of this field. For each video, the matching video clips will be sorted by the level of confidence.
            
            If you set this parameter to `clip_count` and `group_by` is set to `video`, the platform will sort the videos in the response by the number of clips. For each video, the matching video clips will be sorted by the level of confidence. You can use `clip_count` only when the matching video clips are grouped by video.
            
            
            **Default:** `score`
        
        operator : typing.Optional[SearchCreateRequestOperator]
            When you perform a search specifying multiple [sources of information](/v1.3/docs/concepts/modalities#search-options), you can use the this parameter to broaden or narrow your search.
            
              The following logical operators are supported:
            
              - `or`
            
              - `and`
            
              For details and examples, see the [Using multiple sources of information](/v1.3/docs/guides/search/queries/text-queries#visual-and-audio) section.
            
            
              **Default**: `or`.
        
        page_limit : typing.Optional[int]
            The number of items to return on each page. When grouping by video, this parameter represents the number of videos per page. Otherwise, it represents the maximum number of video clips per page.
            
            **Max**: `50`.
        
        filter : typing.Optional[str]
            Specifies a stringified JSON object to filter your search results. Supports both system-generated metadata (example: video ID, duration) and user-defined metadata.
            
            **Syntax for filtering**
            
            The following table describes the supported data types, operators, and filter syntax:
            
            | Data type | Operator | Description | Syntax |
            |:----------|:---------|:------------|:-------|
            | String | `=` | Matches results equal to the specified value. | `{"field": "value"}`
            | Array of strings | `=` | Matches results with any value in the specified array. Supported only for `id`. | `{"id": ["value1", "value2"]}` |
            | Numeric (integer, float) | `=`, `lte`, `gte` | Matches results equal to or within a range of the specified value. | `{"field": number}` or `{"field": { "gte": number, "lte": number }}` |
            | Boolean | `=` | Matches results equal to the specified boolean value. | `{"field": true}` or `{"field": false}`. |
            
            <br/>
            **System-generated metadata**
            
            The table below describes the system-generated metadata available for filtering your  search results:
            
            | Field name | Description | Type | Example |
            |:-----------|:------------|:-----|:--------|
            | `id` | Filters by specific video IDs. | Array of strings | `{"id": ["67cec9caf45d9b64a58340fc", "67cec9baf45d9b64a58340fa"]}`. |
            | `duration` | Filters based on the duration of the video containing the segment that matches your query. | Number or object with `gte` and `lte` | `{"duration": 600}` or `{"duration": { "gte": 600, "lte": 800 }}` |
            | `width` | Filters by video width (in pixels). | Number or object with `gte` and `lte` | `{"width": 1920}` or `{"width": { "gte": 1280, "lte": 1920}}` |
            | `height` | Filters by video height (in pixels). | Number or object with `gte` and `lte`. | `{"height": 1080}` or `{"height": { "gte": 720, "lte": 1080 }}`. |
            | `size` | Filters by video size (in bytes) | Number or object with `gte` and `lte`. | `{"size": 1048576}` or `{"size": { "gte": 1048576, "lte": 5242880}}` |
            | `filename` | Filters by the exact file name. | String | `{"filename": "Animal Encounters part 1"}` |
            
            <br/>
            **User-defined metadata**
            
            To filter by user-defined metadata:
            1. Add metadata to your video by calling the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/:index-id/videos/:video-id` endpoint
            2. Reference the custom field in your filter object. For example, to filter videos where a custom field named `needsReview` of type boolean is `true`, use `{"needs_review": true}`.
            
            For more details and examples, see the [Filter search results](/v1.3/docs/guides/search/filtering) page.
        
        include_user_metadata : typing.Optional[bool]
            Specifies whether to include user-defined metadata in the search results.
        
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.
        
        Returns
        -------
        SearchResults
            Successfully performed a search request.
        
        Examples
        --------
        from twelvelabs import TwelveLabs
        client = TwelveLabs(api_key="YOUR_API_KEY", )
        client.search.create(index_id='index_id', search_options=["visual"], )
        """

        _response = self.create(
            index_id=index_id,
            search_options=search_options,
            query_media_type=query_media_type,
            query_media_url=query_media_url,
            query_media_file=query_media_file,
            query_text=query_text,
            adjust_confidence_level=adjust_confidence_level,
            group_by=group_by,
            threshold=threshold,
            sort_option=sort_option,
            operator=operator,
            page_limit=page_limit,
            filter=filter,
            include_user_metadata=include_user_metadata,
            request_options=request_options,
        )

        _has_next = (
            _response.page_info is not None
            and _response.page_info.next_page_token is not None
        )
        _get_next = lambda: self._get_next_page(_response.page_info.next_page_token)  # type: ignore
        _items = _response.data
        return SyncPager(
            has_next=_has_next, items=_items, get_next=_get_next, response=None
        )

    def __getattr__(self, item):
        return getattr(self.client_wrapper, item)


class AsyncSearchClientWrapper(AsyncSearchClient):
    def __init__(self, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def _get_next_page(self, page_token: str) -> AsyncPager[SearchItem]:
        _response = await self._raw_client._client_wrapper.httpx_client.request(
            f"search/{page_token}",
            method="GET",
        )
        _parsed_response = typing.cast(
            SearchResults,
            parse_obj_as(
                type_=SearchResults,
                object_=_response.json(),
            ),
        )
        _has_next = (
            _parsed_response.page_info is not None
            and _parsed_response.page_info.next_page_token is not None
        )
        _get_next = lambda: self._get_next_page(
            _parsed_response.page_info.next_page_token  # type: ignore
        )
        _items = _parsed_response.data
        return AsyncPager(
            has_next=_has_next, items=_items, get_next=_get_next, response=None
        )

    async def query(
        self,
        *,
        index_id: str,
        search_options: typing.List[SearchCreateRequestSearchOptionsItem],
        query_media_type: typing.Optional[typing.Literal["image"]] = OMIT,
        query_media_url: typing.Optional[str] = OMIT,
        query_media_file: typing.Optional[core.File] = OMIT,
        query_text: typing.Optional[str] = OMIT,
        adjust_confidence_level: typing.Optional[float] = OMIT,
        group_by: typing.Optional[SearchCreateRequestGroupBy] = OMIT,
        threshold: typing.Optional[ThresholdSearch] = OMIT,
        sort_option: typing.Optional[SearchCreateRequestSortOption] = OMIT,
        operator: typing.Optional[SearchCreateRequestOperator] = OMIT,
        page_limit: typing.Optional[int] = OMIT,
        filter: typing.Optional[str] = OMIT,
        include_user_metadata: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncPager[SearchItem]:
        """
        Use this endpoint to search for relevant matches in an index using text or various media queries.
        
        **Text queries**:
        - Use the `query_text` parameter to specify your query.
        
        **Media queries**:
        - Set the `query_media_type` parameter to the corresponding media type (example: `image`).
        - Specify either one of the following parameters:
          - `query_media_url`: Publicly accessible URL of your media file.
          - `query_media_file`: Local media file.
          If both `query_media_url` and `query_media_file` are specified in the same request, `query_media_url` takes precedence.
        <Accordion title="Image requirements">
        Your images must meet the following requirements:
          - **Format**: JPEG and PNG.
          - **Dimension**: Must be at least 64 x 64 pixels.
          - **Size**: Must not exceed 5MB.
          - **Object visibility**: Ensure that the objects of interest are visible and occupy at least 50% of the video frame. This helps the platform accurately identify and match the objects.
        </Accordion>
        
        <Note title="Note">
        This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
        </Note>
        
        Parameters
        ----------
        index_id : str
            The unique identifier of the index to search.
        
        search_options : typing.List[SearchCreateRequestSearchOptionsItem]
            Specifies the [sources of information](/v1.3/docs/concepts/modalities#search-options) the platform uses when performing a search. You must include the `search_options` parameter separately for each desired source of information.
            
            <Note title="Notes">
            - The search options you specify must be a subset of the [model options](/v1.3/docs/concepts/modalities#model-options) used when you created the index.
            - You can specify multiple search options in conjunction with the `operator` parameter described below to broaden or narrow your search.
            
            Example:
            To search using both visual and audio cues, include this parameter twice in the request as shown below:
            ```JSON
            --form search_options=visual \
            --form search_options=audio \
            ```
            </Note>
        
        query_media_type : typing.Optional[typing.Literal["image"]]
            The type of media you wish to use. This parameter is required for media queries. For example, to perform an image-based search, set this parameter to `image`.
        
        query_media_url : typing.Optional[str]
            The publicly accessible URL of the media file you wish to use. This parameter is required for media queries if `query_media_file` is not provided.
        
        query_media_file : typing.Optional[core.File]
            See core.File for more documentation
        
        query_text : typing.Optional[str]
            The text query to search for. This parameter is required for text queries. Note that the platform supports full natural language-based search.
        
        adjust_confidence_level : typing.Optional[float]
            This parameter specifies the strictness of the thresholds for assigning the high, medium, or low confidence levels to search results. If you use a lower value, the thresholds become more relaxed, and more search results will be classified as having high, medium, or low confidence levels. You can use this parameter to include a broader range of potentially relevant video clips, even if some results might be less precise.
            
            **Min**: 0
            **Max**: 1
            **Default:** 0.5
        
        group_by : typing.Optional[SearchCreateRequestGroupBy]
            Use this parameter to group or ungroup items in a response. It can take one of the following values:
            - `video`:  The platform will group the matching video clips in the response by video.
            - `clip`: The matching video clips in the response will not be grouped.
            
            **Default:** `clip`
        
        threshold : typing.Optional[ThresholdSearch]
        
        sort_option : typing.Optional[SearchCreateRequestSortOption]
            Use this parameter to specify the sort order for the response.
            
            When performing a search, the platform determines the level of confidence that each video clip matches your search terms. By default, the search results are sorted on the level of confidence in descending order.
            
            If you set this parameter to `score` and `group_by` is set to `video`, the platform will determine the maximum value of the `score` field for each video and sort the videos in the response by the maximum value of this field. For each video, the matching video clips will be sorted by the level of confidence.
            
            If you set this parameter to `clip_count` and `group_by` is set to `video`, the platform will sort the videos in the response by the number of clips. For each video, the matching video clips will be sorted by the level of confidence. You can use `clip_count` only when the matching video clips are grouped by video.
            
            
            **Default:** `score`
        
        operator : typing.Optional[SearchCreateRequestOperator]
            When you perform a search specifying multiple [sources of information](/v1.3/docs/concepts/modalities#search-options), you can use the this parameter to broaden or narrow your search.
            
              The following logical operators are supported:
            
              - `or`
            
              - `and`
            
              For details and examples, see the [Using multiple sources of information](/v1.3/docs/guides/search/queries/text-queries#visual-and-audio) section.
            
            
              **Default**: `or`.
        
        page_limit : typing.Optional[int]
            The number of items to return on each page. When grouping by video, this parameter represents the number of videos per page. Otherwise, it represents the maximum number of video clips per page.
            
            **Max**: `50`.
        
        filter : typing.Optional[str]
            Specifies a stringified JSON object to filter your search results. Supports both system-generated metadata (example: video ID, duration) and user-defined metadata.
            
            **Syntax for filtering**
            
            The following table describes the supported data types, operators, and filter syntax:
            
            | Data type | Operator | Description | Syntax |
            |:----------|:---------|:------------|:-------|
            | String | `=` | Matches results equal to the specified value. | `{"field": "value"}`
            | Array of strings | `=` | Matches results with any value in the specified array. Supported only for `id`. | `{"id": ["value1", "value2"]}` |
            | Numeric (integer, float) | `=`, `lte`, `gte` | Matches results equal to or within a range of the specified value. | `{"field": number}` or `{"field": { "gte": number, "lte": number }}` |
            | Boolean | `=` | Matches results equal to the specified boolean value. | `{"field": true}` or `{"field": false}`. |
            
            <br/>
            **System-generated metadata**
            
            The table below describes the system-generated metadata available for filtering your  search results:
            
            | Field name | Description | Type | Example |
            |:-----------|:------------|:-----|:--------|
            | `id` | Filters by specific video IDs. | Array of strings | `{"id": ["67cec9caf45d9b64a58340fc", "67cec9baf45d9b64a58340fa"]}`. |
            | `duration` | Filters based on the duration of the video containing the segment that matches your query. | Number or object with `gte` and `lte` | `{"duration": 600}` or `{"duration": { "gte": 600, "lte": 800 }}` |
            | `width` | Filters by video width (in pixels). | Number or object with `gte` and `lte` | `{"width": 1920}` or `{"width": { "gte": 1280, "lte": 1920}}` |
            | `height` | Filters by video height (in pixels). | Number or object with `gte` and `lte`. | `{"height": 1080}` or `{"height": { "gte": 720, "lte": 1080 }}`. |
            | `size` | Filters by video size (in bytes) | Number or object with `gte` and `lte`. | `{"size": 1048576}` or `{"size": { "gte": 1048576, "lte": 5242880}}` |
            | `filename` | Filters by the exact file name. | String | `{"filename": "Animal Encounters part 1"}` |
            
            <br/>
            **User-defined metadata**
            
            To filter by user-defined metadata:
            1. Add metadata to your video by calling the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/:index-id/videos/:video-id` endpoint
            2. Reference the custom field in your filter object. For example, to filter videos where a custom field named `needsReview` of type boolean is `true`, use `{"needs_review": true}`.
            
            For more details and examples, see the [Filter search results](/v1.3/docs/guides/search/filtering) page.
        
        include_user_metadata : typing.Optional[bool]
            Specifies whether to include user-defined metadata in the search results.
        
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.
        
        Returns
        -------
        SearchResults
            Successfully performed a search request.
        
        Examples
        --------
        from twelvelabs import AsyncTwelveLabs
        import asyncio
        client = AsyncTwelveLabs(api_key="YOUR_API_KEY", )
        async def main() -> None:
            await client.search.create(index_id='index_id', search_options=["visual"], )
        asyncio.run(main())
        """

        _response = await self.create(
            index_id=index_id,
            search_options=search_options,
            query_media_type=query_media_type,
            query_media_url=query_media_url,
            query_media_file=query_media_file,
            query_text=query_text,
            adjust_confidence_level=adjust_confidence_level,
            group_by=group_by,
            threshold=threshold,
            sort_option=sort_option,
            operator=operator,
            page_limit=page_limit,
            filter=filter,
            include_user_metadata=include_user_metadata,
            request_options=request_options,
        )

        _has_next = (
            _response.page_info is not None
            and _response.page_info.next_page_token is not None
        )
        _get_next = lambda: self._get_next_page(_response.page_info.next_page_token)  # type: ignore
        _items = _response.data
        return AsyncPager(
            has_next=_has_next, items=_items, get_next=_get_next, response=None
        )

    def __getattr__(self, item):
        return getattr(self.client_wrapper, item)
