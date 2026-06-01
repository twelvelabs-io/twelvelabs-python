"""Tests for ``wait_for_done`` callback behavior (QA-3371).

Regression coverage for the bug where the caller-supplied ``callback`` was only
invoked from inside the polling ``while`` loop. As a result, a task that was
*already terminal* (``ready``/``failed``) at the moment ``wait_for_done`` was
called never fired the callback, and the very first observed status of an
in-progress task was also skipped.

The fix invokes ``callback`` once immediately after the initial fetch, then on
every subsequent poll through the terminal status.

These tests exercise all four implementations:

* ``TaskClientWrapper.wait_for_done`` (sync, uses ``retrieve``)
* ``AsyncTaskClientWrapper.wait_for_done`` (async, uses ``retrieve``)
* ``EmbedTasksClientWrapper.wait_for_done`` (sync, uses ``status``)
* ``AsyncEmbedTasksClientWrapper.wait_for_done`` (async, uses ``status``)
"""

import typing
from unittest import mock

from twelvelabs.embed.tasks.types.tasks_status_response import TasksStatusResponse
from twelvelabs.tasks.types.tasks_retrieve_response import TasksRetrieveResponse
from twelvelabs.wrapper.embed_client_wrapper import (
    AsyncEmbedTasksClientWrapper,
    EmbedTasksClientWrapper,
)
from twelvelabs.wrapper.task_client_wrapper import (
    AsyncTaskClientWrapper,
    TaskClientWrapper,
)

TASK_MODULE = "twelvelabs.wrapper.task_client_wrapper"
EMBED_MODULE = "twelvelabs.wrapper.embed_client_wrapper"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _task_responses(statuses: typing.List[str]) -> typing.List[TasksRetrieveResponse]:
    return [TasksRetrieveResponse(status=status) for status in statuses]


def _embed_responses(statuses: typing.List[str]) -> typing.List[TasksStatusResponse]:
    return [TasksStatusResponse(status=status) for status in statuses]


def _make_sync_task_wrapper(
    statuses: typing.List[str],
) -> typing.Tuple[TaskClientWrapper, mock.Mock]:
    # Bypass __init__ (which needs a real client wrapper) and stub the fetch.
    wrapper = TaskClientWrapper.__new__(TaskClientWrapper)
    fetch = mock.Mock(side_effect=_task_responses(statuses))
    setattr(wrapper, "retrieve", fetch)
    return wrapper, fetch


def _make_async_task_wrapper(
    statuses: typing.List[str],
) -> typing.Tuple[AsyncTaskClientWrapper, mock.AsyncMock]:
    wrapper = AsyncTaskClientWrapper.__new__(AsyncTaskClientWrapper)
    fetch = mock.AsyncMock(side_effect=_task_responses(statuses))
    setattr(wrapper, "retrieve", fetch)
    return wrapper, fetch


def _make_sync_embed_wrapper(
    statuses: typing.List[str],
) -> typing.Tuple[EmbedTasksClientWrapper, mock.Mock]:
    wrapper = EmbedTasksClientWrapper.__new__(EmbedTasksClientWrapper)
    fetch = mock.Mock(side_effect=_embed_responses(statuses))
    setattr(wrapper, "status", fetch)
    return wrapper, fetch


def _make_async_embed_wrapper(
    statuses: typing.List[str],
) -> typing.Tuple[AsyncEmbedTasksClientWrapper, mock.AsyncMock]:
    wrapper = AsyncEmbedTasksClientWrapper.__new__(AsyncEmbedTasksClientWrapper)
    fetch = mock.AsyncMock(side_effect=_embed_responses(statuses))
    setattr(wrapper, "status", fetch)
    return wrapper, fetch


# --------------------------------------------------------------------------- #
# sync TaskClientWrapper.wait_for_done
# --------------------------------------------------------------------------- #
def test_sync_task_already_ready_fires_callback_once() -> None:
    wrapper, fetch = _make_sync_task_wrapper(["ready"])
    callback = mock.Mock()

    with mock.patch(f"{TASK_MODULE}.time.sleep") as sleep_mock:
        result = wrapper.wait_for_done(task_id="t", callback=callback)

    assert result.status == "ready"
    callback.assert_called_once_with(result)
    sleep_mock.assert_not_called()
    assert fetch.call_count == 1


def test_sync_task_already_failed_fires_callback_once() -> None:
    wrapper, fetch = _make_sync_task_wrapper(["failed"])
    callback = mock.Mock()

    with mock.patch(f"{TASK_MODULE}.time.sleep") as sleep_mock:
        result = wrapper.wait_for_done(task_id="t", callback=callback)

    assert result.status == "failed"
    callback.assert_called_once_with(result)
    sleep_mock.assert_not_called()
    assert fetch.call_count == 1


def test_sync_task_progress_sequence_fires_each_status() -> None:
    wrapper, fetch = _make_sync_task_wrapper(["pending", "indexing", "ready"])
    observed: typing.List[str] = []
    callback = mock.Mock(side_effect=lambda task: observed.append(task.status))

    with mock.patch(f"{TASK_MODULE}.time.sleep") as sleep_mock:
        result = wrapper.wait_for_done(
            task_id="t", sleep_interval=1.0, callback=callback
        )

    assert observed == ["pending", "indexing", "ready"]
    assert result.status == "ready"
    assert sleep_mock.call_count == 2
    assert fetch.call_count == 3


def test_sync_task_callback_none_already_ready() -> None:
    wrapper, fetch = _make_sync_task_wrapper(["ready"])

    with mock.patch(f"{TASK_MODULE}.time.sleep") as sleep_mock:
        result = wrapper.wait_for_done(task_id="t", callback=None)

    assert result.status == "ready"
    sleep_mock.assert_not_called()
    assert fetch.call_count == 1


# --------------------------------------------------------------------------- #
# async AsyncTaskClientWrapper.wait_for_done
# --------------------------------------------------------------------------- #
async def test_async_task_already_ready_fires_callback_once() -> None:
    wrapper, fetch = _make_async_task_wrapper(["ready"])
    callback = mock.AsyncMock()

    with mock.patch(
        f"{TASK_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock
    ) as sleep_mock:
        result = await wrapper.wait_for_done(task_id="t", callback=callback)

    assert result.status == "ready"
    callback.assert_awaited_once_with(result)
    sleep_mock.assert_not_awaited()
    assert fetch.await_count == 1


async def test_async_task_already_failed_fires_callback_once() -> None:
    wrapper, fetch = _make_async_task_wrapper(["failed"])
    callback = mock.AsyncMock()

    with mock.patch(
        f"{TASK_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock
    ) as sleep_mock:
        result = await wrapper.wait_for_done(task_id="t", callback=callback)

    assert result.status == "failed"
    callback.assert_awaited_once_with(result)
    sleep_mock.assert_not_awaited()
    assert fetch.await_count == 1


async def test_async_task_progress_sequence_fires_each_status() -> None:
    wrapper, fetch = _make_async_task_wrapper(["pending", "indexing", "ready"])
    observed: typing.List[str] = []

    async def callback(task: TasksRetrieveResponse) -> None:
        observed.append(typing.cast(str, task.status))

    with mock.patch(
        f"{TASK_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock
    ) as sleep_mock:
        result = await wrapper.wait_for_done(
            task_id="t", sleep_interval=1.0, callback=callback
        )

    assert observed == ["pending", "indexing", "ready"]
    assert result.status == "ready"
    assert sleep_mock.await_count == 2
    assert fetch.await_count == 3


async def test_async_task_callback_none_already_ready() -> None:
    wrapper, fetch = _make_async_task_wrapper(["ready"])

    with mock.patch(
        f"{TASK_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock
    ) as sleep_mock:
        result = await wrapper.wait_for_done(task_id="t", callback=None)

    assert result.status == "ready"
    sleep_mock.assert_not_awaited()
    assert fetch.await_count == 1


async def test_async_task_async_callback_is_awaited() -> None:
    wrapper, _ = _make_async_task_wrapper(["ready"])
    callback = mock.AsyncMock()

    with mock.patch(f"{TASK_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock):
        result = await wrapper.wait_for_done(task_id="t", callback=callback)

    # An async callback must be awaited, not merely called.
    callback.assert_awaited_once_with(result)


# --------------------------------------------------------------------------- #
# sync EmbedTasksClientWrapper.wait_for_done
# --------------------------------------------------------------------------- #
def test_sync_embed_already_ready_fires_callback_once() -> None:
    wrapper, fetch = _make_sync_embed_wrapper(["ready"])
    callback = mock.Mock()

    with mock.patch(f"{EMBED_MODULE}.time.sleep") as sleep_mock:
        result = wrapper.wait_for_done(task_id="t", callback=callback)

    assert result.status == "ready"
    callback.assert_called_once_with(result)
    sleep_mock.assert_not_called()
    assert fetch.call_count == 1


def test_sync_embed_already_failed_fires_callback_once() -> None:
    wrapper, fetch = _make_sync_embed_wrapper(["failed"])
    callback = mock.Mock()

    with mock.patch(f"{EMBED_MODULE}.time.sleep") as sleep_mock:
        result = wrapper.wait_for_done(task_id="t", callback=callback)

    assert result.status == "failed"
    callback.assert_called_once_with(result)
    sleep_mock.assert_not_called()
    assert fetch.call_count == 1


def test_sync_embed_progress_sequence_fires_each_status() -> None:
    wrapper, fetch = _make_sync_embed_wrapper(["processing", "processing", "ready"])
    observed: typing.List[str] = []
    callback = mock.Mock(side_effect=lambda task: observed.append(task.status))

    with mock.patch(f"{EMBED_MODULE}.time.sleep") as sleep_mock:
        result = wrapper.wait_for_done(
            task_id="t", sleep_interval=1.0, callback=callback
        )

    assert observed == ["processing", "processing", "ready"]
    assert result.status == "ready"
    assert sleep_mock.call_count == 2
    assert fetch.call_count == 3


def test_sync_embed_callback_none_already_ready() -> None:
    wrapper, fetch = _make_sync_embed_wrapper(["ready"])

    with mock.patch(f"{EMBED_MODULE}.time.sleep") as sleep_mock:
        result = wrapper.wait_for_done(task_id="t", callback=None)

    assert result.status == "ready"
    sleep_mock.assert_not_called()
    assert fetch.call_count == 1


# --------------------------------------------------------------------------- #
# async AsyncEmbedTasksClientWrapper.wait_for_done
# --------------------------------------------------------------------------- #
async def test_async_embed_already_ready_fires_callback_once() -> None:
    wrapper, fetch = _make_async_embed_wrapper(["ready"])
    callback = mock.AsyncMock()

    with mock.patch(
        f"{EMBED_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock
    ) as sleep_mock:
        result = await wrapper.wait_for_done(task_id="t", callback=callback)

    assert result.status == "ready"
    callback.assert_awaited_once_with(result)
    sleep_mock.assert_not_awaited()
    assert fetch.await_count == 1


async def test_async_embed_already_failed_fires_callback_once() -> None:
    wrapper, fetch = _make_async_embed_wrapper(["failed"])
    callback = mock.AsyncMock()

    with mock.patch(
        f"{EMBED_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock
    ) as sleep_mock:
        result = await wrapper.wait_for_done(task_id="t", callback=callback)

    assert result.status == "failed"
    callback.assert_awaited_once_with(result)
    sleep_mock.assert_not_awaited()
    assert fetch.await_count == 1


async def test_async_embed_progress_sequence_fires_each_status() -> None:
    wrapper, fetch = _make_async_embed_wrapper(["processing", "processing", "ready"])
    observed: typing.List[str] = []

    async def callback(task: TasksStatusResponse) -> None:
        observed.append(typing.cast(str, task.status))

    with mock.patch(
        f"{EMBED_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock
    ) as sleep_mock:
        result = await wrapper.wait_for_done(
            task_id="t", sleep_interval=1.0, callback=callback
        )

    assert observed == ["processing", "processing", "ready"]
    assert result.status == "ready"
    assert sleep_mock.await_count == 2
    assert fetch.await_count == 3


async def test_async_embed_callback_none_already_ready() -> None:
    wrapper, fetch = _make_async_embed_wrapper(["ready"])

    with mock.patch(
        f"{EMBED_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock
    ) as sleep_mock:
        result = await wrapper.wait_for_done(task_id="t", callback=None)

    assert result.status == "ready"
    sleep_mock.assert_not_awaited()
    assert fetch.await_count == 1


async def test_async_embed_async_callback_is_awaited() -> None:
    wrapper, _ = _make_async_embed_wrapper(["ready"])
    callback = mock.AsyncMock()

    with mock.patch(f"{EMBED_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock):
        result = await wrapper.wait_for_done(task_id="t", callback=callback)

    # An async callback must be awaited, not merely called.
    callback.assert_awaited_once_with(result)


# --------------------------------------------------------------------------- #
# Retry path: a failed re-fetch is retried (`continue`) WITHOUT firing the
# callback. This branch lives inside the polling loop that the fix reorganizes,
# so it is exercised for both the sync/`time` path (task wrapper) and the
# async/`asyncio` path (embed wrapper); the other two methods are structurally
# identical. These also pin the fetch call arguments.
# --------------------------------------------------------------------------- #
def test_sync_task_retry_on_fetch_error_does_not_fire_callback() -> None:
    wrapper = TaskClientWrapper.__new__(TaskClientWrapper)
    fetch = mock.Mock(
        side_effect=[
            TasksRetrieveResponse(status="pending"),
            RuntimeError("transient"),
            TasksRetrieveResponse(status="ready"),
        ]
    )
    setattr(wrapper, "retrieve", fetch)
    observed: typing.List[str] = []
    callback = mock.Mock(side_effect=lambda task: observed.append(task.status))

    with mock.patch(f"{TASK_MODULE}.time.sleep") as sleep_mock:
        result = wrapper.wait_for_done(
            task_id="t", sleep_interval=1.0, callback=callback
        )

    # Callback fires for the initial `pending` and terminal `ready`, but NOT for
    # the iteration whose re-fetch raised (that iteration hits `continue`).
    assert observed == ["pending", "ready"]
    assert result.status == "ready"
    assert fetch.call_count == 3
    assert sleep_mock.call_count == 2
    fetch.assert_called_with("t", request_options=None)


async def test_async_embed_retry_on_fetch_error_does_not_fire_callback() -> None:
    wrapper = AsyncEmbedTasksClientWrapper.__new__(AsyncEmbedTasksClientWrapper)
    fetch = mock.AsyncMock(
        side_effect=[
            TasksStatusResponse(status="processing"),
            RuntimeError("transient"),
            TasksStatusResponse(status="ready"),
        ]
    )
    setattr(wrapper, "status", fetch)
    observed: typing.List[str] = []

    async def callback(task: TasksStatusResponse) -> None:
        observed.append(typing.cast(str, task.status))

    with mock.patch(
        f"{EMBED_MODULE}.asyncio.sleep", new_callable=mock.AsyncMock
    ) as sleep_mock:
        result = await wrapper.wait_for_done(
            task_id="t", sleep_interval=1.0, callback=callback
        )

    assert observed == ["processing", "ready"]
    assert result.status == "ready"
    assert fetch.await_count == 3
    assert sleep_mock.await_count == 2
    fetch.assert_awaited_with("t", request_options=None)
