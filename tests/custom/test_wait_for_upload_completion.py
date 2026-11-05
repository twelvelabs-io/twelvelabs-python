import typing
from unittest.mock import MagicMock

import httpx
import pytest

from twelvelabs.wrapper import multipart_upload_client_wrapper as upload_wrapper
from twelvelabs.wrapper.multipart_upload_client_wrapper import (
    AsyncMultipartUploadClientWrapper,
    MultipartUploadClientWrapper,
    UploadError,
)


class _StillPolling(BaseException):
    """Stops a polling loop that ignores max_wait_time, so the test fails instead of hanging."""


class _FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0
        self.sleeps: typing.List[float] = []

    def time(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds

    async def async_sleep(self, seconds: float) -> None:
        self.sleep(seconds)


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> _FakeClock:
    fake = _FakeClock()
    monkeypatch.setattr(upload_wrapper.time, "time", fake.time)
    monkeypatch.setattr(upload_wrapper.time, "sleep", fake.sleep)
    monkeypatch.setattr(upload_wrapper.asyncio, "sleep", fake.async_sleep)
    return fake


def test_wait_for_upload_completion_times_out_when_status_keeps_failing(clock: _FakeClock) -> None:
    client = MultipartUploadClientWrapper(client_wrapper=MagicMock())
    calls = []

    def get_status(upload_id: str, **kwargs: typing.Any) -> typing.Any:
        calls.append(upload_id)
        if len(calls) > 50:
            raise _StillPolling()
        raise httpx.ConnectError("connection refused")

    client.get_status = get_status  # type: ignore[method-assign]

    with pytest.raises(UploadError, match="timed out"):
        client.wait_for_upload_completion("upload-id", sleep_interval=10.0, max_wait_time=30.0)

    assert len(calls) <= 5
    assert all(seconds == 10.0 for seconds in clock.sleeps)


async def test_async_wait_for_upload_completion_times_out_when_status_keeps_failing(clock: _FakeClock) -> None:
    client = AsyncMultipartUploadClientWrapper(client_wrapper=MagicMock())
    calls = []

    async def get_status(upload_id: str, **kwargs: typing.Any) -> typing.Any:
        calls.append(upload_id)
        if len(calls) > 50:
            raise _StillPolling()
        raise httpx.ConnectError("connection refused")

    client.get_status = get_status  # type: ignore[method-assign]

    with pytest.raises(UploadError, match="timed out"):
        await client.wait_for_upload_completion("upload-id", sleep_interval=10.0, max_wait_time=30.0)

    assert len(calls) <= 5
    assert all(seconds == 10.0 for seconds in clock.sleeps)
