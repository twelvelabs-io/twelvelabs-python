import typing
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from ..core.http_response import BaseHttpResponse
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pagination import SyncPager, AsyncPager
from ..core.pydantic_utilities import parse_obj_as
from ..core.request_options import RequestOptions
from ..types.video_vector import VideoVector
from ..indexes.client import IndexesClient, AsyncIndexesClient
from ..indexes.videos.client import VideosClient, AsyncVideosClient
from ..indexes.videos.types.videos_list_request_user_metadata_value import (
    VideosListRequestUserMetadataValue,
)
from ..indexes.videos.types.videos_list_response import VideosListResponse
from ..errors.bad_request_error import BadRequestError

OMIT = typing.cast(typing.Any, ...)


class VideosClientWrapper(VideosClient):
    """Wrapper for the VideosClient that adds additional functionality."""

    def __init__(self, client_wrapper: SyncClientWrapper):
        """Initialize the VideosClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)

    def list(
        self,
        index_id: str,
        *,
        page: typing.Optional[int] = None,
        page_limit: typing.Optional[int] = None,
        sort_by: typing.Optional[str] = None,
        sort_option: typing.Optional[str] = None,
        filename: typing.Optional[str] = None,
        duration: typing.Optional[float] = None,
        fps: typing.Optional[float] = None,
        width: typing.Optional[float] = None,
        height: typing.Optional[int] = None,
        size: typing.Optional[float] = None,
        created_at: typing.Optional[str] = None,
        updated_at: typing.Optional[str] = None,
        user_metadata: typing.Optional[
            typing.Dict[str, typing.Optional[VideosListRequestUserMetadataValue]]
        ] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SyncPager[VideoVector]:
        """
        This method returns a list of the videos in the specified index. By default, the API returns your videos sorted by creation date, with the newest at the top of the list.

        Parameters
        ----------
        index_id : str
            The unique identifier of the index for which the API will retrieve the videos.

        page : typing.Optional[int]
            A number that identifies the page to retrieve.

            **Default**: `1`.

        page_limit : typing.Optional[int]
            The number of items to return on each page.

            **Default**: `10`.
            **Max**: `50`.

        sort_by : typing.Optional[str]
            The field to sort on. The following options are available:
            - `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was updated.
            - `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was created.

            **Default**: `created_at`.

        sort_option : typing.Optional[str]
            The sorting direction. The following options are available:
            - `asc`
            - `desc`

            **Default**: `desc`.

        filename : typing.Optional[str]
            Filter by filename.

        duration : typing.Optional[float]
            Filter by duration. Expressed in seconds.

        fps : typing.Optional[float]
            Filter by frames per second.

        width : typing.Optional[float]
            Filter by width.

        height : typing.Optional[int]
            Filter by height.

        size : typing.Optional[float]
            Filter by size. Expressed in bytes.

        created_at : typing.Optional[str]
            Filter videos by the creation date and time of their associated indexing tasks, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the videos whose indexing tasks were created on the specified date at or after the given time.

        updated_at : typing.Optional[str]
            This filter applies only to videos updated using the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/{index-id}/videos/{video-id}` endpoint. It filters videos by the last update date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the video indexing tasks that were last updated on the specified date at or after the given time.

        user_metadata : typing.Optional[typing.Dict[str, typing.Optional[VideosListRequestUserMetadataValue]]]
            To enable filtering by custom fields, you must first add user-defined metadata to your video by calling the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/:index-id/videos/:video-id` endpoint.

            Examples:
            - To filter on a string: `?category=recentlyAdded`
            - To filter on an integer: `?batchNumber=5`
            - To filter on a float: `?rating=9.3`
            - To filter on a boolean: `?needsReview=true`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        SyncPager[VideoVector]
            The video vectors in the specified index have successfully been retrieved.

        Examples
        --------
        from twelvelabs import TwelveLabs
        client = TwelveLabs(api_key="YOUR_API_KEY", )
        response = client.indexes.videos.list(index_id='6298d673f1090f1100476d4c', page=1, page_limit=10, sort_by='created_at', sort_option='desc', filename='01.mp4', created_at='2024-08-16T16:53:59Z', updated_at='2024-08-16T16:53:59Z', )
        for item in response:
            yield item
        # alternatively, you can paginate page-by-page
        for page in response.iter_pages():
            yield page
        """
        page = page if page is not None else 1

        # Build params dict
        params = {
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
            "filename": filename,
            "duration": duration,
            "fps": fps,
            "width": width,
            "height": height,
            "size": size,
            "created_at": created_at,
            "updated_at": updated_at,
        }

        # Flatten user_metadata into root level parameters
        if user_metadata:
            for key, value in user_metadata.items():
                params[key] = value

        _response = self._raw_client._client_wrapper.httpx_client.request(
            f"indexes/{jsonable_encoder(index_id)}/videos",
            method="GET",
            params=params,
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _parsed_response = typing.cast(
                    VideosListResponse,
                    parse_obj_as(
                        type_=VideosListResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                _items = _parsed_response.data
                _has_next = True
                _get_next = lambda: self.list(
                    index_id,
                    page=page + 1,
                    page_limit=page_limit,
                    sort_by=sort_by,
                    sort_option=sort_option,
                    filename=filename,
                    duration=duration,
                    fps=fps,
                    width=width,
                    height=height,
                    size=size,
                    created_at=created_at,
                    updated_at=updated_at,
                    user_metadata=user_metadata,
                    request_options=request_options,
                )
                return SyncPager(
                    has_next=_has_next,
                    items=_items,
                    get_next=_get_next,
                    response=BaseHttpResponse(response=_response),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(
                status_code=_response.status_code,
                headers=dict(_response.headers),
                body=_response.text,
            )
        raise ApiError(
            status_code=_response.status_code,
            headers=dict(_response.headers),
            body=_response_json,
        )


class AsyncVideosClientWrapper(AsyncVideosClient):
    """Async wrapper for the VideosClient that adds additional functionality."""

    def __init__(self, client_wrapper: AsyncClientWrapper):
        """Initialize the AsyncVideosClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)

    async def list(
        self,
        index_id: str,
        *,
        page: typing.Optional[int] = None,
        page_limit: typing.Optional[int] = None,
        sort_by: typing.Optional[str] = None,
        sort_option: typing.Optional[str] = None,
        filename: typing.Optional[str] = None,
        duration: typing.Optional[float] = None,
        fps: typing.Optional[float] = None,
        width: typing.Optional[float] = None,
        height: typing.Optional[int] = None,
        size: typing.Optional[float] = None,
        created_at: typing.Optional[str] = None,
        updated_at: typing.Optional[str] = None,
        user_metadata: typing.Optional[
            typing.Dict[str, typing.Optional[VideosListRequestUserMetadataValue]]
        ] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncPager[VideoVector]:
        """
        This method returns a list of the videos in the specified index. By default, the API returns your videos sorted by creation date, with the newest at the top of the list.

        Parameters
        ----------
        index_id : str
            The unique identifier of the index for which the API will retrieve the videos.

        page : typing.Optional[int]
            A number that identifies the page to retrieve.

            **Default**: `1`.

        page_limit : typing.Optional[int]
            The number of items to return on each page.

            **Default**: `10`.
            **Max**: `50`.

        sort_by : typing.Optional[str]
            The field to sort on. The following options are available:
            - `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was updated.
            - `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was created.

            **Default**: `created_at`.

        sort_option : typing.Optional[str]
            The sorting direction. The following options are available:
            - `asc`
            - `desc`

            **Default**: `desc`.

        filename : typing.Optional[str]
            Filter by filename.

        duration : typing.Optional[float]
            Filter by duration. Expressed in seconds.

        fps : typing.Optional[float]
            Filter by frames per second.

        width : typing.Optional[float]
            Filter by width.

        height : typing.Optional[int]
            Filter by height.

        size : typing.Optional[float]
            Filter by size. Expressed in bytes.

        created_at : typing.Optional[str]
            Filter videos by the creation date and time of their associated indexing tasks, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the videos whose indexing tasks were created on the specified date at or after the given time.

        updated_at : typing.Optional[str]
            This filter applies only to videos updated using the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/{index-id}/videos/{video-id}` endpoint. It filters videos by the last update date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the video indexing tasks that were last updated on the specified date at or after the given time.

        user_metadata : typing.Optional[typing.Dict[str, typing.Optional[VideosListRequestUserMetadataValue]]]
            To enable filtering by custom fields, you must first add user-defined metadata to your video by calling the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/:index-id/videos/:video-id` endpoint.

            Examples:
            - To filter on a string: `?category=recentlyAdded`
            - To filter on an integer: `?batchNumber=5`
            - To filter on a float: `?rating=9.3`
            - To filter on a boolean: `?needsReview=true`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncPager[VideoVector]
            The video vectors in the specified index have successfully been retrieved.

        Examples
        --------
        from twelvelabs import AsyncTwelveLabs
        import asyncio
        client = AsyncTwelveLabs(api_key="YOUR_API_KEY", )
        async def main() -> None:
            response = await client.indexes.videos.list(index_id='6298d673f1090f1100476d4c', page=1, page_limit=10, sort_by='created_at', sort_option='desc', filename='01.mp4', created_at='2024-08-16T16:53:59Z', updated_at='2024-08-16T16:53:59Z', )
            async for item in response:
                yield item

            # alternatively, you can paginate page-by-page
            async for page in response.iter_pages():
                yield page
        asyncio.run(main())
        """
        page = page if page is not None else 1

        # Build params dict
        params = {
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
            "filename": filename,
            "duration": duration,
            "fps": fps,
            "width": width,
            "height": height,
            "size": size,
            "created_at": created_at,
            "updated_at": updated_at,
        }

        # Flatten user_metadata into root level parameters
        if user_metadata:
            for key, value in user_metadata.items():
                params[key] = value

        _response = await self._raw_client._client_wrapper.httpx_client.request(
            f"indexes/{jsonable_encoder(index_id)}/videos",
            method="GET",
            params=params,
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _parsed_response = typing.cast(
                    VideosListResponse,
                    parse_obj_as(
                        type_=VideosListResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                _items = _parsed_response.data
                _has_next = True

                async def _get_next():
                    return await self.list(
                        index_id,
                        page=page + 1,
                        page_limit=page_limit,
                        sort_by=sort_by,
                        sort_option=sort_option,
                        filename=filename,
                        duration=duration,
                        fps=fps,
                        width=width,
                        height=height,
                        size=size,
                        created_at=created_at,
                        updated_at=updated_at,
                        user_metadata=user_metadata,
                        request_options=request_options,
                    )

                return AsyncPager(
                    has_next=_has_next,
                    items=_items,
                    get_next=_get_next,
                    response=BaseHttpResponse(response=_response),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(
                status_code=_response.status_code,
                headers=dict(_response.headers),
                body=_response.text,
            )
        raise ApiError(
            status_code=_response.status_code,
            headers=dict(_response.headers),
            body=_response_json,
        )


class IndexesClientWrapper(IndexesClient):
    """Wrapper for the IndexesClient that adds custom functionality."""

    def __init__(self, client_wrapper: SyncClientWrapper):
        """Initialize the IndexesClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)
        # Replace the videos property with our custom implementation
        self.videos = VideosClientWrapper(client_wrapper=client_wrapper)


class AsyncIndexesClientWrapper(AsyncIndexesClient):
    """Async wrapper for the IndexesClient that adds custom functionality."""

    def __init__(self, client_wrapper: AsyncClientWrapper):
        """Initialize the AsyncIndexesClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)
        # Replace the videos property with our custom implementation
        self.videos = AsyncVideosClientWrapper(client_wrapper=client_wrapper)
