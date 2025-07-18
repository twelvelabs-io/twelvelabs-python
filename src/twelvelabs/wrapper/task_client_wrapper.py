import typing
import time
import asyncio
from ..core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from ..tasks.client import TasksClient, AsyncTasksClient
from ..tasks.types.tasks_create_response import TasksCreateResponse
from ..tasks.types.tasks_retrieve_response import TasksRetrieveResponse
from ..core.request_options import RequestOptions
from .. import core

OMIT = typing.cast(typing.Any, ...)


class TaskClientWrapper(TasksClient):
    """Wrapper for the TasksClient that adds additional functionality."""

    def __init__(self, client_wrapper: SyncClientWrapper):
        """Initialize the TaskClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)

    def create_bulk(
        self,
        *,
        index_id: str,
        video_files: typing.Optional[typing.List[core.File]] = None,
        video_urls: typing.Optional[typing.List[str]] = None,
        enable_video_stream: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[TasksCreateResponse]:
        """
        This method creates multiple video indexing tasks that upload and index videos in bulk.
        Ensure your videos meet the requirements in the Prerequisites section of the Upload single videos page.

        Upload options:
        - **Local files**: Use the `video_files` parameter to provide a list of files.
        - **Publicly accessible URLs**: Use the `video_urls` parameter to provide a list of URLs.

        Parameters
        ----------
        index_id : str
            The unique identifier of the index to which the videos are being uploaded.

        video_files : typing.Optional[typing.List[core.File]]
            A list of video files to upload and index.

        video_urls : typing.Optional[typing.List[str]]
            A list of publicly accessible URLs of videos to upload and index.

        enable_video_stream : typing.Optional[bool]
            This parameter indicates if the platform stores the videos for streaming.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[TasksCreateResponse]
            A list of video indexing tasks that were successfully created.

        Examples
        --------
        from twelvelabs import TwelveLabs

        client = TwelveLabs(
            api_key="YOUR_API_KEY",
        )
        client.tasks.create_bulk(
            index_id="index_id",
            video_urls=["https://example.com/video1.mp4", "https://example.com/video2.mp4"],
        )
        """
        if not video_files and not video_urls:
            raise ValueError("Either video_files or video_urls must be provided")

        tasks = []

        if video_files:
            for video_file in video_files:
                try:
                    task = self.create(
                        index_id=index_id,
                        video_file=video_file,
                        enable_video_stream=enable_video_stream,
                        request_options=request_options,
                    )
                    tasks.append(task)
                except Exception as e:
                    print(f"Error processing file: {e}")
                    continue

        if video_urls:
            for video_url in video_urls:
                try:
                    task = self.create(
                        index_id=index_id,
                        video_url=video_url,
                        enable_video_stream=enable_video_stream,
                        request_options=request_options,
                    )
                    tasks.append(task)
                except Exception as e:
                    print(f"Error processing url {video_url}: {e}")
                    continue

        return tasks

    def wait_for_done(
        self,
        task_id: str,
        *,
        sleep_interval: float = 5.0,
        callback: typing.Optional[
            typing.Callable[[TasksRetrieveResponse], None]
        ] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TasksRetrieveResponse:
        """
        Wait for a task to complete by periodically checking its status.

        Parameters
        ----------
        task_id : str
            The unique identifier of the task to wait for.

        sleep_interval : float, optional
            The time in seconds to wait between status checks, by default 5.0

        callback : typing.Optional[typing.Callable[[TasksRetrieveResponse], None]], optional
            A function to call after each status check with the task response, by default None

        request_options : typing.Optional[RequestOptions], optional
            Request-specific configuration, by default None

        Returns
        -------
        TasksRetrieveResponse
            The completed task response

        Raises
        ------
        ValueError
            If sleep_interval is less than or equal to 0

        Examples
        --------
        from twelvelabs import TwelveLabs

        client = TwelveLabs(
            api_key="YOUR_API_KEY",
        )
        task = client.tasks.create(index_id="index_id", video_url="https://example.com/video.mp4")
        completed_task = client.tasks.wait_for_done(
            task_id=task._id,
            sleep_interval=10.0,
            callback=lambda task: print(f"Current status: {task.status}")
        )
        """
        if sleep_interval <= 0:
            raise ValueError("sleep_interval must be greater than 0")

        # Get initial task
        task = self.retrieve(task_id, request_options=request_options)

        # Check if it's already done
        done_statuses = ["ready", "failed"]

        # Continue checking until it's done
        while task.status not in done_statuses:
            time.sleep(sleep_interval)

            try:
                task = self.retrieve(task_id, request_options=request_options)
            except Exception as e:
                print(f"Retrieving task failed: {e}. Retrying...")
                continue

            if callback is not None:
                callback(task)

        return task


class AsyncTaskClientWrapper(AsyncTasksClient):
    """Async wrapper for the TasksClient that adds additional functionality."""

    def __init__(self, client_wrapper: AsyncClientWrapper):
        """Initialize the AsyncTaskClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)

    async def create_bulk(
        self,
        *,
        index_id: str,
        video_files: typing.Optional[typing.List[core.File]] = None,
        video_urls: typing.Optional[typing.List[str]] = None,
        enable_video_stream: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[TasksCreateResponse]:
        """
        This method creates multiple video indexing tasks that upload and index videos in bulk.
        Ensure your videos meet the requirements in the Prerequisites section of the Upload single videos page.

        Upload options:
        - **Local files**: Use the `video_files` parameter to provide a list of files.
        - **Publicly accessible URLs**: Use the `video_urls` parameter to provide a list of URLs.

        Parameters
        ----------
        index_id : str
            The unique identifier of the index to which the videos are being uploaded.

        video_files : typing.Optional[typing.List[core.File]]
            A list of video files to upload and index.

        video_urls : typing.Optional[typing.List[str]]
            A list of publicly accessible URLs of videos to upload and index.

        enable_video_stream : typing.Optional[bool]
            This parameter indicates if the platform stores the videos for streaming.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[TasksCreateResponse]
            A list of video indexing tasks that were successfully created.

        Examples
        --------
        import asyncio

        from twelvelabs import AsyncTwelveLabs

        client = AsyncTwelveLabs(
            api_key="YOUR_API_KEY",
        )

        async def main() -> None:
            tasks = await client.tasks.create_bulk(
                index_id="index_id",
                video_urls=["https://example.com/video1.mp4", "https://example.com/video2.mp4"],
            )
            print(tasks)

        asyncio.run(main())
        """
        if not video_files and not video_urls:
            raise ValueError("Either video_files or video_urls must be provided")

        tasks = []

        if video_files:
            for video_file in video_files:
                try:
                    task = await self.create(
                        index_id=index_id,
                        video_file=video_file,
                        enable_video_stream=enable_video_stream,
                        request_options=request_options,
                    )
                    tasks.append(task)
                except Exception as e:
                    print(f"Error processing file: {e}")
                    continue

        if video_urls:
            for video_url in video_urls:
                try:
                    task = await self.create(
                        index_id=index_id,
                        video_url=video_url,
                        enable_video_stream=enable_video_stream,
                        request_options=request_options,
                    )
                    tasks.append(task)
                except Exception as e:
                    print(f"Error processing url {video_url}: {e}")
                    continue

        return tasks

    async def wait_for_done(
        self,
        task_id: str,
        *,
        sleep_interval: float = 5.0,
        callback: typing.Optional[
            typing.Callable[[TasksRetrieveResponse], typing.Awaitable[None]]
        ] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TasksRetrieveResponse:
        """
        Wait for a task to complete by periodically checking its status.

        Parameters
        ----------
        task_id : str
            The unique identifier of the task to wait for.

        sleep_interval : float, optional
            The time in seconds to wait between status checks, by default 5.0

        callback : typing.Optional[typing.Callable[[TasksRetrieveResponse], typing.Awaitable[None]]], optional
            An async function to call after each status check with the task response, by default None

        request_options : typing.Optional[RequestOptions], optional
            Request-specific configuration, by default None

        Returns
        -------
        TasksRetrieveResponse
            The completed task response

        Raises
        ------
        ValueError
            If sleep_interval is less than or equal to 0

        Examples
        --------
        import asyncio
        from twelvelabs import AsyncTwelveLabs

        client = AsyncTwelveLabs(
            api_key="YOUR_API_KEY",
        )

        async def status_callback(task):
            print(f"Current status: {task.status}")

        async def main() -> None:
            task = await client.tasks.create(index_id="index_id", video_url="https://example.com/video.mp4")
            completed_task = await client.tasks.wait_for_done(
                task_id=task._id,
                sleep_interval=10.0,
                callback=status_callback
            )
            print(f"Task completed with status: {completed_task.status}")

        asyncio.run(main())
        """
        if sleep_interval <= 0:
            raise ValueError("sleep_interval must be greater than 0")

        # Get initial task
        task = await self.retrieve(task_id, request_options=request_options)

        # Check if it's already done
        done_statuses = ["ready", "failed"]

        # Continue checking until it's done
        while task.status not in done_statuses:
            await asyncio.sleep(sleep_interval)

            try:
                task = await self.retrieve(task_id, request_options=request_options)
            except Exception as e:
                print(f"Retrieving task failed: {e}. Retrying...")
                continue

            if callback is not None:
                await callback(task)

        return task
