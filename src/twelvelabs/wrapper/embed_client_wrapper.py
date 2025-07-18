import typing
import time
import asyncio
from ..core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from ..embed.client import EmbedClient, AsyncEmbedClient
from ..embed.tasks.client import TasksClient, AsyncTasksClient
from ..embed.tasks.types.tasks_create_response import TasksCreateResponse
from ..embed.tasks.types.tasks_status_response import TasksStatusResponse
from ..embed.tasks.types.tasks_create_request_video_embedding_scope_item import (
    TasksCreateRequestVideoEmbeddingScopeItem,
)
from ..core.request_options import RequestOptions
from .. import core

OMIT = typing.cast(typing.Any, ...)


class CreateEmbeddingsTaskVideoParams(typing.TypedDict, total=False):
    """Parameters for creating a video embedding task."""

    video_file: typing.Optional[core.File]
    video_url: typing.Optional[str]
    video_start_offset_sec: typing.Optional[float]
    video_end_offset_sec: typing.Optional[float]
    video_clip_length: typing.Optional[int]
    video_embedding_scope: typing.Optional[
        typing.List[TasksCreateRequestVideoEmbeddingScopeItem]
    ]


class EmbedTasksClientWrapper(TasksClient):
    """Wrapper for the TasksClient that adds additional functionality."""

    def __init__(self, client_wrapper: SyncClientWrapper):
        """Initialize the EmbedTasksClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)

    def create_bulk(
        self,
        *,
        model_name: typing.Literal["Marengo-retrieval-2.7"],
        videos: typing.List[CreateEmbeddingsTaskVideoParams],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[TasksCreateResponse]:
        """
        This method creates multiple video embedding tasks in bulk.

        Parameters
        ----------
        model_name : typing.Literal["Marengo-retrieval-2.7"]
            The name of the embedding model to use.

        videos : typing.List[CreateEmbeddingsTaskVideoParams]
            A list of video parameters for creating embedding tasks. Each item should have:
            - video_file or video_url: The video file or URL to embed
            - Optional parameters like start/end offsets, clip length, and embedding scopes

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[TasksCreateResponse]
            A list of video embedding tasks that were successfully created.

        Examples
        --------
        from twelvelabs import TwelveLabs
        from twelvelabs.wrapper.embed_client_wrapper import CreateEmbeddingsTaskVideoParams

        client = TwelveLabs(
            api_key="YOUR_API_KEY",
        )

        videos = [
            CreateEmbeddingsTaskVideoParams(
                video_url="https://example.com/video1.mp4",
                video_embedding_scopes=["clip", "video"]
            ),
            CreateEmbeddingsTaskVideoParams(
                video_url="https://example.com/video2.mp4",
                video_embedding_scopes=["clip"]
            )
        ]

        tasks = client.embed.tasks.create_bulk(
            model_name="Marengo-retrieval-2.7",
            videos=videos,
        )
        """
        tasks = []

        for video_params in videos:
            try:
                # Extract parameters, handling both dict and object access
                def get_param(key: str) -> typing.Any:
                    if hasattr(video_params, key):
                        return getattr(video_params, key)
                    return (
                        video_params.get(key)
                        if isinstance(video_params, dict)
                        else None
                    )

                # Build kwargs, only including non-None values
                kwargs: typing.Dict[str, typing.Any] = {"model_name": model_name}

                video_file = get_param("video_file")
                if video_file is not None:
                    kwargs["video_file"] = video_file

                video_url = get_param("video_url")
                if video_url is not None:
                    kwargs["video_url"] = video_url

                video_start_offset_sec = get_param("video_start_offset_sec")
                if video_start_offset_sec is not None:
                    kwargs["video_start_offset_sec"] = video_start_offset_sec

                video_end_offset_sec = get_param("video_end_offset_sec")
                if video_end_offset_sec is not None:
                    kwargs["video_end_offset_sec"] = video_end_offset_sec

                video_clip_length = get_param("video_clip_length")
                if video_clip_length is not None:
                    kwargs["video_clip_length"] = video_clip_length

                video_embedding_scope = get_param("video_embedding_scope")
                if video_embedding_scope is not None:
                    kwargs["video_embedding_scope"] = video_embedding_scope

                if request_options is not None:
                    kwargs["request_options"] = request_options

                task = self.create(**kwargs)
                tasks.append(task)
            except Exception as e:
                print(f"Error creating embedding task: {e}")
                continue

        return tasks

    def wait_for_done(
        self,
        task_id: str,
        *,
        sleep_interval: float = 5.0,
        callback: typing.Optional[typing.Callable[[TasksStatusResponse], None]] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TasksStatusResponse:
        """
        Wait for a task to complete by periodically checking its status.

        Parameters
        ----------
        task_id : str
            The unique identifier of the task to wait for.

        sleep_interval : float, optional
            The time in seconds to wait between status checks, by default 5.0

        callback : typing.Optional[typing.Callable[[TasksStatusResponse], None]], optional
            A function to call after each status check with the task response, by default None

        Returns
        -------
        TasksStatusResponse
            The completed task response

        Examples
        --------
        from twelvelabs import TwelveLabs

        client = TwelveLabs(
            api_key="YOUR_API_KEY",
        )

        task = client.embed.tasks.create(
            model_name="Marengo-retrieval-2.7",
            video_url="https://example.com/video.mp4",
        )

        completed_task = client.embed.tasks.wait_for_done(
            task_id=task._id,
            sleep_interval=10.0,
        )
        """
        if sleep_interval <= 0:
            raise ValueError("sleep_interval must be greater than 0")

        # Get initial task
        task = self.status(task_id, request_options=request_options)

        # Check if it's already done
        done_statuses = ["ready", "failed"]

        while task.status not in done_statuses:
            time.sleep(sleep_interval)

            try:
                task = self.status(task_id, request_options=request_options)
            except Exception as e:
                print(f"Retrieving task status failed: {e}. Retrying...")
                continue

            if callback is not None:
                callback(task)

        return task


class AsyncEmbedTasksClientWrapper(AsyncTasksClient):
    """Async wrapper for the TasksClient that adds additional functionality."""

    def __init__(self, client_wrapper: AsyncClientWrapper):
        """Initialize the AsyncEmbedTasksClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)

    async def create_bulk(
        self,
        *,
        model_name: typing.Literal["Marengo-retrieval-2.7"],
        videos: typing.List[CreateEmbeddingsTaskVideoParams],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[TasksCreateResponse]:
        """
        This method creates multiple video embedding tasks in bulk.

        Parameters
        ----------
        model_name : typing.Literal["Marengo-retrieval-2.7"]
            The name of the embedding model to use.

        videos : typing.List[CreateEmbeddingsTaskVideoParams]
            A list of video parameters for creating embedding tasks. Each item should have:
            - video_file or video_url: The video file or URL to embed
            - Optional parameters like start/end offsets, clip length, and embedding scopes

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[TasksCreateResponse]
            A list of video embedding tasks that were successfully created.

        Examples
        --------
        import asyncio
        from twelvelabs import AsyncTwelveLabs
        from twelvelabs.wrapper.embed_client_wrapper import CreateEmbeddingsTaskVideoParams

        client = AsyncTwelveLabs(
            api_key="YOUR_API_KEY",
        )

        async def main() -> None:
            videos = [
                CreateEmbeddingsTaskVideoParams(
                    video_url="https://example.com/video1.mp4",
                    video_embedding_scopes=["clip", "video"]
                ),
                CreateEmbeddingsTaskVideoParams(
                    video_url="https://example.com/video2.mp4",
                    video_embedding_scopes=["clip"]
                )
            ]

            tasks = await client.embed.tasks.create_bulk(
                model_name="Marengo-retrieval-2.7",
                videos=videos,
            )
            print(tasks)

        asyncio.run(main())
        """
        tasks = []

        for video_params in videos:
            try:
                # Extract parameters, handling both dict and object access
                def get_param(key: str) -> typing.Any:
                    if hasattr(video_params, key):
                        return getattr(video_params, key)
                    return (
                        video_params.get(key)
                        if isinstance(video_params, dict)
                        else None
                    )

                # Build kwargs, only including non-None values
                kwargs: typing.Dict[str, typing.Any] = {"model_name": model_name}

                video_file = get_param("video_file")
                if video_file is not None:
                    kwargs["video_file"] = video_file

                video_url = get_param("video_url")
                if video_url is not None:
                    kwargs["video_url"] = video_url

                video_start_offset_sec = get_param("video_start_offset_sec")
                if video_start_offset_sec is not None:
                    kwargs["video_start_offset_sec"] = video_start_offset_sec

                video_end_offset_sec = get_param("video_end_offset_sec")
                if video_end_offset_sec is not None:
                    kwargs["video_end_offset_sec"] = video_end_offset_sec

                video_clip_length = get_param("video_clip_length")
                if video_clip_length is not None:
                    kwargs["video_clip_length"] = video_clip_length

                video_embedding_scope = get_param("video_embedding_scope")
                if video_embedding_scope is not None:
                    kwargs["video_embedding_scope"] = video_embedding_scope

                if request_options is not None:
                    kwargs["request_options"] = request_options

                task = await self.create(**kwargs)
                tasks.append(task)
            except Exception as e:
                print(f"Error creating embedding task: {e}")
                continue

        return tasks

    async def wait_for_done(
        self,
        task_id: str,
        *,
        sleep_interval: float = 5.0,
        callback: typing.Optional[
            typing.Callable[[TasksStatusResponse], typing.Awaitable[None]]
        ] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TasksStatusResponse:
        """
        Wait for a task to complete by periodically checking its status.

        Parameters
        ----------
        task_id : str
            The unique identifier of the task to wait for.

        sleep_interval : float, optional
            The time in seconds to wait between status checks, by default 5.0

        callback : typing.Optional[typing.Callable[[TasksStatusResponse], typing.Awaitable[None]]], optional
            A function to call after each status check with the task response, by default None

        Returns
        -------
        TasksStatusResponse
            The completed task response

        Examples
        --------
        import asyncio
        from twelvelabs import AsyncTwelveLabs

        client = AsyncTwelveLabs(
            api_key="YOUR_API_KEY",
        )

        task = await client.embed.tasks.create(
            model_name="Marengo-retrieval-2.7",
            video_url="https://example.com/video.mp4",
        )

        completed_task = await client.embed.tasks.wait_for_done(
            task_id=task._id,
            sleep_interval=10.0,
        )
        """
        if sleep_interval <= 0:
            raise ValueError("sleep_interval must be greater than 0")

        # Get initial task
        task = await self.status(task_id, request_options=request_options)

        # Check if it's already done
        done_statuses = ["ready", "failed"]

        while task.status not in done_statuses:
            await asyncio.sleep(sleep_interval)

            try:
                task = await self.status(task_id, request_options=request_options)
            except Exception as e:
                print(f"Retrieving task status failed: {e}. Retrying...")
                continue

            if callback is not None:
                await callback(task)

        return task


class EmbedClientWrapper(EmbedClient):
    """Wrapper for the EmbedClient that adds custom functionality."""

    def __init__(self, client_wrapper: SyncClientWrapper):
        """Initialize the EmbedClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)
        # Replace the tasks property with our custom implementation
        self.tasks = EmbedTasksClientWrapper(client_wrapper=client_wrapper)


class AsyncEmbedClientWrapper(AsyncEmbedClient):
    """Async wrapper for the EmbedClient that adds custom functionality."""

    def __init__(self, client_wrapper: AsyncClientWrapper):
        """Initialize the AsyncEmbedClientWrapper."""
        super().__init__(client_wrapper=client_wrapper)
        # Replace the tasks property with our custom implementation
        self.tasks = AsyncEmbedTasksClientWrapper(client_wrapper=client_wrapper)
