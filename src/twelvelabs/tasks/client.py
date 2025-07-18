# This file was auto-generated by Fern from our API Definition.

import typing

from .. import core
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.pagination import AsyncPager, SyncPager
from ..core.request_options import RequestOptions
from ..types.video_indexing_task import VideoIndexingTask
from .raw_client import AsyncRawTasksClient, RawTasksClient
from .transfers.client import AsyncTransfersClient, TransfersClient
from .types.tasks_create_response import TasksCreateResponse
from .types.tasks_list_request_status_item import TasksListRequestStatusItem
from .types.tasks_retrieve_response import TasksRetrieveResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class TasksClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._raw_client = RawTasksClient(client_wrapper=client_wrapper)
        self.transfers = TransfersClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> RawTasksClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        RawTasksClient
        """
        return self._raw_client

    def list(
        self,
        *,
        page: typing.Optional[int] = None,
        page_limit: typing.Optional[int] = None,
        sort_by: typing.Optional[str] = None,
        sort_option: typing.Optional[str] = None,
        index_id: typing.Optional[str] = None,
        status: typing.Optional[
            typing.Union[TasksListRequestStatusItem, typing.Sequence[TasksListRequestStatusItem]]
        ] = None,
        filename: typing.Optional[str] = None,
        duration: typing.Optional[float] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        created_at: typing.Optional[str] = None,
        updated_at: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SyncPager[VideoIndexingTask]:
        """
        This method returns a list of the video indexing tasks in your account. The API returns your video indexing tasks sorted by creation date, with the newest at the top of the list.

        Parameters
        ----------
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

        index_id : typing.Optional[str]
            Filter by the unique identifier of an index.

        status : typing.Optional[typing.Union[TasksListRequestStatusItem, typing.Sequence[TasksListRequestStatusItem]]]
            Filter by one or more video indexing task statuses. The following options are available:
            - `ready`: The video has been successfully uploaded and indexed.
            - `uploading`: The video is being uploaded.
            - `validating`: The video is being validated against the prerequisites.
            - `pending`: The video is pending.
            - `queued`: The video is queued.
            - `indexing`: The video is being indexed.
            - `failed`: The video indexing task failed.

            To filter by multiple statuses, specify the `status` parameter for each value:
            ```
            status=ready&status=validating
            ```

        filename : typing.Optional[str]
            Filter by filename.

        duration : typing.Optional[float]
            Filter by duration. Expressed in seconds.

        width : typing.Optional[int]
            Filter by width.

        height : typing.Optional[int]
            Filter by height.

        created_at : typing.Optional[str]
            Filter video indexing tasks by the creation date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the video indexing tasks that were created on the specified date at or after the given time.

        updated_at : typing.Optional[str]
            Filter video indexing tasks by the last update date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the video indexing tasks that were updated on the specified date at or after the given time.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        SyncPager[VideoIndexingTask]
            The video indexing tasks have successfully been retrieved.

        Examples
        --------
        from twelvelabs import TwelveLabs
        client = TwelveLabs(api_key="YOUR_API_KEY", )
        response = client.tasks.list(page=1, page_limit=10, sort_by='created_at', sort_option='desc', index_id='630aff993fcee0532cb809d0', filename='01.mp4', duration=531.998133, width=640, height=360, created_at='2024-03-01T00:00:00Z', updated_at='2024-03-01T00:00:00Z', )
        for item in response:
            yield item
        # alternatively, you can paginate page-by-page
        for page in response.iter_pages():
            yield page
        """
        return self._raw_client.list(
            page=page,
            page_limit=page_limit,
            sort_by=sort_by,
            sort_option=sort_option,
            index_id=index_id,
            status=status,
            filename=filename,
            duration=duration,
            width=width,
            height=height,
            created_at=created_at,
            updated_at=updated_at,
            request_options=request_options,
        )

    def create(
        self,
        *,
        index_id: str,
        video_file: typing.Optional[core.File] = OMIT,
        video_url: typing.Optional[str] = OMIT,
        enable_video_stream: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TasksCreateResponse:
        """
        This method creates a video indexing task that uploads and indexes a video.

        Upload options:
        - **Local file**: Use the `video_file` parameter.
        - **Publicly accessible URL**: Use the `video_url` parameter.

        <Accordion title="Video requirements">
          The videos you wish to upload must meet the following requirements:
          - **Video resolution**: Must be at least 360x360 and must not exceed 3840x2160.
          - **Aspect ratio**: Must be one of 1:1, 4:3, 4:5, 5:4, 16:9, 9:16, or 17:9.
          - **Video and audio formats**: Your video files must be encoded in the video and audio formats listed on the [FFmpeg Formats Documentation](https://ffmpeg.org/ffmpeg-formats.html) page. For videos in other formats, contact us at support@twelvelabs.io.
          - **Duration**: For Marengo, it must be between 4 seconds and 2 hours (7,200s). For Pegasus, it must be between 4 seconds and 60 minutes (3600s). In a future release, the maximum duration for Pegasus will be 2 hours (7,200 seconds).
          - **File size**: Must not exceed 2 GB.
            If you require different options, contact us at support@twelvelabs.io.

          If both Marengo and Pegasus are enabled for your index, the most restrictive prerequisites will apply.
        </Accordion>

        <Note title="Notes">
        - The platform supports video URLs that can play without additional user interaction or custom video players. Ensure your URL points to the raw video file, not a web page containing the video. Links to third-party hosting sites, cloud storage services, or videos requiring extra steps to play are not supported.
        - This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
        </Note>

        Parameters
        ----------
        index_id : str
            The unique identifier of the index to which the video is being uploaded.

        video_file : typing.Optional[core.File]
            See core.File for more documentation

        video_url : typing.Optional[str]
            Specify this parameter to upload a video from a publicly accessible URL.

        enable_video_stream : typing.Optional[bool]
            This parameter indicates if the platform stores the video for streaming. When set to `true`, the platform stores the video, and you can retrieve its URL by calling the [`GET`](/v1.3/api-reference/videos/retrieve) method of the `/indexes/{index-id}/videos/{video-id}` endpoint. You can then use this URL to access the stream over the <a href="https://en.wikipedia.org/wiki/HTTP_Live_Streaming" target="_blank">HLS</a> protocol.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TasksCreateResponse
            A video indexing task has successfully been created.

        Examples
        --------
        from twelvelabs import TwelveLabs
        client = TwelveLabs(api_key="YOUR_API_KEY", )
        client.tasks.create(index_id='index_id', )
        """
        _response = self._raw_client.create(
            index_id=index_id,
            video_file=video_file,
            video_url=video_url,
            enable_video_stream=enable_video_stream,
            request_options=request_options,
        )
        return _response.data

    def retrieve(
        self, task_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> TasksRetrieveResponse:
        """
        This method retrieves a video indexing task.

        Parameters
        ----------
        task_id : str
            The unique identifier of the video indexing task to retrieve.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TasksRetrieveResponse
            The specified video indexing task has successfully been retrieved.

        Examples
        --------
        from twelvelabs import TwelveLabs
        client = TwelveLabs(api_key="YOUR_API_KEY", )
        client.tasks.retrieve(task_id='6298d673f1090f1100476d4c', )
        """
        _response = self._raw_client.retrieve(task_id, request_options=request_options)
        return _response.data

    def delete(self, task_id: str, *, request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        This action cannot be undone.
        Note the following about deleting a video indexing task:
        - You can only delete video indexing tasks for which the status is `ready` or `failed`.
        - If the status of your video indexing task is `ready`, you must first delete the video vector associated with your video indexing task by calling the [`DELETE`](/v1.3/api-reference/videos/delete) method of the `/indexes/videos` endpoint.

        Parameters
        ----------
        task_id : str
            The unique identifier of the video indexing task you want to delete.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from twelvelabs import TwelveLabs
        client = TwelveLabs(api_key="YOUR_API_KEY", )
        client.tasks.delete(task_id='6298d673f1090f1100476d4c', )
        """
        _response = self._raw_client.delete(task_id, request_options=request_options)
        return _response.data


class AsyncTasksClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._raw_client = AsyncRawTasksClient(client_wrapper=client_wrapper)
        self.transfers = AsyncTransfersClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> AsyncRawTasksClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        AsyncRawTasksClient
        """
        return self._raw_client

    async def list(
        self,
        *,
        page: typing.Optional[int] = None,
        page_limit: typing.Optional[int] = None,
        sort_by: typing.Optional[str] = None,
        sort_option: typing.Optional[str] = None,
        index_id: typing.Optional[str] = None,
        status: typing.Optional[
            typing.Union[TasksListRequestStatusItem, typing.Sequence[TasksListRequestStatusItem]]
        ] = None,
        filename: typing.Optional[str] = None,
        duration: typing.Optional[float] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        created_at: typing.Optional[str] = None,
        updated_at: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncPager[VideoIndexingTask]:
        """
        This method returns a list of the video indexing tasks in your account. The API returns your video indexing tasks sorted by creation date, with the newest at the top of the list.

        Parameters
        ----------
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

        index_id : typing.Optional[str]
            Filter by the unique identifier of an index.

        status : typing.Optional[typing.Union[TasksListRequestStatusItem, typing.Sequence[TasksListRequestStatusItem]]]
            Filter by one or more video indexing task statuses. The following options are available:
            - `ready`: The video has been successfully uploaded and indexed.
            - `uploading`: The video is being uploaded.
            - `validating`: The video is being validated against the prerequisites.
            - `pending`: The video is pending.
            - `queued`: The video is queued.
            - `indexing`: The video is being indexed.
            - `failed`: The video indexing task failed.

            To filter by multiple statuses, specify the `status` parameter for each value:
            ```
            status=ready&status=validating
            ```

        filename : typing.Optional[str]
            Filter by filename.

        duration : typing.Optional[float]
            Filter by duration. Expressed in seconds.

        width : typing.Optional[int]
            Filter by width.

        height : typing.Optional[int]
            Filter by height.

        created_at : typing.Optional[str]
            Filter video indexing tasks by the creation date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the video indexing tasks that were created on the specified date at or after the given time.

        updated_at : typing.Optional[str]
            Filter video indexing tasks by the last update date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the video indexing tasks that were updated on the specified date at or after the given time.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncPager[VideoIndexingTask]
            The video indexing tasks have successfully been retrieved.

        Examples
        --------
        from twelvelabs import AsyncTwelveLabs
        import asyncio
        client = AsyncTwelveLabs(api_key="YOUR_API_KEY", )
        async def main() -> None:
            response = await client.tasks.list(page=1, page_limit=10, sort_by='created_at', sort_option='desc', index_id='630aff993fcee0532cb809d0', filename='01.mp4', duration=531.998133, width=640, height=360, created_at='2024-03-01T00:00:00Z', updated_at='2024-03-01T00:00:00Z', )
            async for item in response:
                yield item

            # alternatively, you can paginate page-by-page
            async for page in response.iter_pages():
                yield page
        asyncio.run(main())
        """
        return await self._raw_client.list(
            page=page,
            page_limit=page_limit,
            sort_by=sort_by,
            sort_option=sort_option,
            index_id=index_id,
            status=status,
            filename=filename,
            duration=duration,
            width=width,
            height=height,
            created_at=created_at,
            updated_at=updated_at,
            request_options=request_options,
        )

    async def create(
        self,
        *,
        index_id: str,
        video_file: typing.Optional[core.File] = OMIT,
        video_url: typing.Optional[str] = OMIT,
        enable_video_stream: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TasksCreateResponse:
        """
        This method creates a video indexing task that uploads and indexes a video.

        Upload options:
        - **Local file**: Use the `video_file` parameter.
        - **Publicly accessible URL**: Use the `video_url` parameter.

        <Accordion title="Video requirements">
          The videos you wish to upload must meet the following requirements:
          - **Video resolution**: Must be at least 360x360 and must not exceed 3840x2160.
          - **Aspect ratio**: Must be one of 1:1, 4:3, 4:5, 5:4, 16:9, 9:16, or 17:9.
          - **Video and audio formats**: Your video files must be encoded in the video and audio formats listed on the [FFmpeg Formats Documentation](https://ffmpeg.org/ffmpeg-formats.html) page. For videos in other formats, contact us at support@twelvelabs.io.
          - **Duration**: For Marengo, it must be between 4 seconds and 2 hours (7,200s). For Pegasus, it must be between 4 seconds and 60 minutes (3600s). In a future release, the maximum duration for Pegasus will be 2 hours (7,200 seconds).
          - **File size**: Must not exceed 2 GB.
            If you require different options, contact us at support@twelvelabs.io.

          If both Marengo and Pegasus are enabled for your index, the most restrictive prerequisites will apply.
        </Accordion>

        <Note title="Notes">
        - The platform supports video URLs that can play without additional user interaction or custom video players. Ensure your URL points to the raw video file, not a web page containing the video. Links to third-party hosting sites, cloud storage services, or videos requiring extra steps to play are not supported.
        - This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
        </Note>

        Parameters
        ----------
        index_id : str
            The unique identifier of the index to which the video is being uploaded.

        video_file : typing.Optional[core.File]
            See core.File for more documentation

        video_url : typing.Optional[str]
            Specify this parameter to upload a video from a publicly accessible URL.

        enable_video_stream : typing.Optional[bool]
            This parameter indicates if the platform stores the video for streaming. When set to `true`, the platform stores the video, and you can retrieve its URL by calling the [`GET`](/v1.3/api-reference/videos/retrieve) method of the `/indexes/{index-id}/videos/{video-id}` endpoint. You can then use this URL to access the stream over the <a href="https://en.wikipedia.org/wiki/HTTP_Live_Streaming" target="_blank">HLS</a> protocol.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TasksCreateResponse
            A video indexing task has successfully been created.

        Examples
        --------
        from twelvelabs import AsyncTwelveLabs
        import asyncio
        client = AsyncTwelveLabs(api_key="YOUR_API_KEY", )
        async def main() -> None:
            await client.tasks.create(index_id='index_id', )
        asyncio.run(main())
        """
        _response = await self._raw_client.create(
            index_id=index_id,
            video_file=video_file,
            video_url=video_url,
            enable_video_stream=enable_video_stream,
            request_options=request_options,
        )
        return _response.data

    async def retrieve(
        self, task_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> TasksRetrieveResponse:
        """
        This method retrieves a video indexing task.

        Parameters
        ----------
        task_id : str
            The unique identifier of the video indexing task to retrieve.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TasksRetrieveResponse
            The specified video indexing task has successfully been retrieved.

        Examples
        --------
        from twelvelabs import AsyncTwelveLabs
        import asyncio
        client = AsyncTwelveLabs(api_key="YOUR_API_KEY", )
        async def main() -> None:
            await client.tasks.retrieve(task_id='6298d673f1090f1100476d4c', )
        asyncio.run(main())
        """
        _response = await self._raw_client.retrieve(task_id, request_options=request_options)
        return _response.data

    async def delete(self, task_id: str, *, request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        This action cannot be undone.
        Note the following about deleting a video indexing task:
        - You can only delete video indexing tasks for which the status is `ready` or `failed`.
        - If the status of your video indexing task is `ready`, you must first delete the video vector associated with your video indexing task by calling the [`DELETE`](/v1.3/api-reference/videos/delete) method of the `/indexes/videos` endpoint.

        Parameters
        ----------
        task_id : str
            The unique identifier of the video indexing task you want to delete.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from twelvelabs import AsyncTwelveLabs
        import asyncio
        client = AsyncTwelveLabs(api_key="YOUR_API_KEY", )
        async def main() -> None:
            await client.tasks.delete(task_id='6298d673f1090f1100476d4c', )
        asyncio.run(main())
        """
        _response = await self._raw_client.delete(task_id, request_options=request_options)
        return _response.data
