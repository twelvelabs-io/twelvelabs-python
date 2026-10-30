import json
import typing

import httpx
import pydantic
import pytest

from twelvelabs import AsyncTwelveLabs, TwelveLabs
from twelvelabs.errors import NotFoundError

BATCH_ID = "68d3ae81c4a8d3697e15b2ef"
ITEM = {"task_id": "task-1", "custom_id": "first", "status": "ready", "data": []}


def read_results(client, raw):
    if raw:
        with client.embed.v_2.batches.with_raw_response.results(BATCH_ID) as response:
            assert response.headers["x-request-id"] == "request-1"
            return list(response.data)
    return list(client.embed.v_2.batches.results(BATCH_ID))


async def read_results_async(client, raw):
    if raw:
        async with client.embed.v_2.batches.with_raw_response.results(BATCH_ID) as response:
            assert response.headers["x-request-id"] == "request-1"
            return [item async for item in response.data]
    return [item async for item in client.embed.v_2.batches.results(BATCH_ID)]


def transport(payload, responses, status=200):
    def handle(request):
        assert request.url.path == "/v1.3/embed-v2/batches/" + BATCH_ID + "/results"
        assert request.headers["x-api-key"] == "test-key"
        response = httpx.Response(
            status,
            stream=httpx.ByteStream(payload),
            headers={"x-request-id": "request-1", "content-type": "application/x-ndjson"},
        )
        responses.append(response)
        return response

    return httpx.MockTransport(handle)


class BrokenStream(httpx.SyncByteStream, httpx.AsyncByteStream):
    def __iter__(self):
        yield json.dumps(ITEM).encode() + b"\n"
        raise httpx.ReadError("connection interrupted")

    async def __aiter__(self):
        yield json.dumps(ITEM).encode() + b"\n"
        raise httpx.ReadError("connection interrupted")


class OneByteAtATimeStream(httpx.SyncByteStream, httpx.AsyncByteStream):
    def __init__(self, payload):
        self._payload = payload

    def __iter__(self):
        for index in range(len(self._payload)):
            yield self._payload[index : index + 1]

    async def __aiter__(self):
        for index in range(len(self._payload)):
            yield self._payload[index : index + 1]


class StopAfterFirstLineStream(httpx.SyncByteStream, httpx.AsyncByteStream):
    def __init__(self, payload):
        self._payload = payload
        self.read_after_line = False

    def __iter__(self):
        for index in range(len(self._payload)):
            chunk = self._payload[index : index + 1]
            yield chunk
            if chunk == b"\n":
                self.read_after_line = True
                raise AssertionError("read continued after the first JSONL record")

    async def __aiter__(self):
        for index in range(len(self._payload)):
            chunk = self._payload[index : index + 1]
            yield chunk
            if chunk == b"\n":
                self.read_after_line = True
                raise AssertionError("read continued after the first JSONL record")


class TrackingResponse(httpx.Response):
    byte_iterator_closed: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.byte_iterator_closed = False

    def iter_bytes(self, chunk_size: typing.Optional[int] = None) -> typing.Iterator[bytes]:
        byte_stream = typing.cast(
            typing.Generator[bytes, None, None], super().iter_bytes(chunk_size=chunk_size)
        )

        def track() -> typing.Iterator[bytes]:
            try:
                yield from byte_stream
            finally:
                byte_stream.close()
                self.byte_iterator_closed = True

        return track()

    def aiter_bytes(self, chunk_size: typing.Optional[int] = None) -> typing.AsyncIterator[bytes]:
        byte_stream = typing.cast(
            typing.AsyncGenerator[bytes, None], super().aiter_bytes(chunk_size=chunk_size)
        )

        async def track() -> typing.AsyncGenerator[bytes, None]:
            try:
                async for chunk in byte_stream:
                    yield chunk
            finally:
                await byte_stream.aclose()
                self.byte_iterator_closed = True

        return track()


def chunked_transport(
    payload,
    responses,
    response_class=httpx.Response,
    stream_class=OneByteAtATimeStream,
    streams=None,
):
    def handle(request):
        assert request.url.path == "/v1.3/embed-v2/batches/" + BATCH_ID + "/results"
        stream = stream_class(payload)
        if streams is not None:
            streams.append(stream)
        response = response_class(
            200,
            stream=stream,
            headers={"x-request-id": "request-1", "content-type": "application/x-ndjson"},
        )
        responses.append(response)
        return response

    return httpx.MockTransport(handle)


@pytest.fixture(autouse=True)
def shutdown_async_generators(event_loop):
    yield
    event_loop.run_until_complete(event_loop.shutdown_asyncgens())


@pytest.mark.parametrize("raw", [False, True])
def test_sync_preserves_lines_and_future_status(raw):
    responses = []
    future = dict(ITEM, task_id="task-2", custom_id="second", status="future_status", future_field="kept")
    payload = ("\n" + json.dumps(ITEM) + "\r\n\n" + json.dumps(future)).encode()
    with httpx.Client(transport=transport(payload, responses)) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        items = read_results(client, raw)
        assert [(item.custom_id, item.status) for item in items] == [("first", "ready"), ("second", "future_status")]
        assert items[1].dict()["future_field"] == "kept"
        assert responses[0].is_closed


@pytest.mark.parametrize("raw", [False, True])
@pytest.mark.parametrize(
    "bad_line,error",
    [(b'{"task_id":', json.JSONDecodeError), (b'{"status":"ready"}', pydantic.ValidationError)],
)
def test_sync_does_not_drop_invalid_lines(raw, bad_line, error):
    responses = []
    payload = json.dumps(ITEM).encode() + b"\n" + bad_line
    with httpx.Client(transport=transport(payload, responses)) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        with pytest.raises(error):
            read_results(client, raw)
        assert responses[0].is_closed


@pytest.mark.parametrize("raw", [False, True])
def test_sync_retains_generated_http_error(raw):
    responses = []
    body = {"code": "resource_not_exists", "message": "Not found"}
    with httpx.Client(transport=transport(json.dumps(body).encode(), responses, status=404)) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        with pytest.raises(NotFoundError) as exc:
            read_results(client, raw)
        assert exc.value.body == body
        assert exc.value.headers["x-request-id"] == "request-1"
        assert responses[0].is_closed


@pytest.mark.parametrize("raw", [False, True])
def test_sync_propagates_interrupted_stream(raw):
    responses = []

    def handle(request):
        response = httpx.Response(200, stream=BrokenStream(), headers={"x-request-id": "request-1"})
        responses.append(response)
        return response

    with httpx.Client(transport=httpx.MockTransport(handle)) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        with pytest.raises(httpx.ReadError, match="connection interrupted"):
            read_results(client, raw)
        assert responses[0].is_closed


@pytest.mark.asyncio
@pytest.mark.parametrize("raw", [False, True])
async def test_async_preserves_lines_and_future_status(raw):
    responses = []
    future = dict(ITEM, task_id="task-2", custom_id="second", status="future_status", future_field="kept")
    payload = ("\n" + json.dumps(ITEM) + "\r\n\n" + json.dumps(future)).encode()
    async with httpx.AsyncClient(transport=transport(payload, responses)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        items = await read_results_async(client, raw)
        assert [(item.custom_id, item.status) for item in items] == [("first", "ready"), ("second", "future_status")]
        assert items[1].dict()["future_field"] == "kept"
        assert responses[0].is_closed


@pytest.mark.asyncio
@pytest.mark.parametrize("raw", [False, True])
@pytest.mark.parametrize(
    "bad_line,error",
    [(b'{"task_id":', json.JSONDecodeError), (b'{"status":"ready"}', pydantic.ValidationError)],
)
async def test_async_does_not_drop_invalid_lines(raw, bad_line, error):
    responses = []
    payload = json.dumps(ITEM).encode() + b"\n" + bad_line
    async with httpx.AsyncClient(transport=transport(payload, responses)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        with pytest.raises(error):
            await read_results_async(client, raw)
        assert responses[0].is_closed


@pytest.mark.asyncio
@pytest.mark.parametrize("raw", [False, True])
async def test_async_retains_generated_http_error(raw):
    responses = []
    body = {"code": "resource_not_exists", "message": "Not found"}
    async with httpx.AsyncClient(transport=transport(json.dumps(body).encode(), responses, status=404)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        with pytest.raises(NotFoundError) as exc:
            await read_results_async(client, raw)
        assert exc.value.body == body
        assert exc.value.headers["x-request-id"] == "request-1"
        assert responses[0].is_closed


@pytest.mark.asyncio
@pytest.mark.parametrize("raw", [False, True])
async def test_async_propagates_interrupted_stream(raw):
    responses = []

    def handle(request):
        response = httpx.Response(200, stream=BrokenStream(), headers={"x-request-id": "request-1"})
        responses.append(response)
        return response

    async with httpx.AsyncClient(transport=httpx.MockTransport(handle)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        with pytest.raises(httpx.ReadError, match="connection interrupted"):
            await read_results_async(client, raw)
        assert responses[0].is_closed


@pytest.mark.parametrize("raw", [False, True])
def test_sync_frames_lf_bytes_and_preserves_split_utf8_and_json_line_separator(raw):
    responses = []
    first = dict(ITEM, custom_id="café\u2028東京", data=[{"embedding": [0.125, -0.5]}])
    second = dict(ITEM, task_id="task-2", custom_id="second")
    payload = (
        json.dumps(first, ensure_ascii=False).encode("utf-8")
        + b"\r\n\r\n"
        + json.dumps(second, ensure_ascii=False).encode("utf-8")
    )
    with httpx.Client(transport=chunked_transport(payload, responses)) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        items = read_results(client, raw)

    assert [item.custom_id for item in items] == ["café\u2028東京", "second"]
    assert items[0].data[0].embedding == [0.125, -0.5]
    assert responses[0].is_closed


@pytest.mark.parametrize("raw", [False, True])
@pytest.mark.parametrize(
    "payload",
    [
        b'{"task_id":"task-1","custom_id":"bad\xffid","status":"ready","data":[]}\n',
        b'{"task_id":"task-1","custom_id":"caf\xc3',
    ],
)
def test_sync_rejects_malformed_or_truncated_utf8_and_closes_response(raw, payload):
    responses = []
    streams = []
    if payload.endswith(b"\n"):
        payload += json.dumps(ITEM).encode() + b"\n"
    with httpx.Client(
        transport=chunked_transport(
            payload, responses, TrackingResponse, StopAfterFirstLineStream, streams
        )
    ) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        with pytest.raises(UnicodeDecodeError):
            read_results(client, raw)

    assert responses[0].is_closed
    assert typing.cast(TrackingResponse, responses[0]).byte_iterator_closed
    assert not streams[0].read_after_line


@pytest.mark.asyncio
@pytest.mark.parametrize("raw", [False, True])
async def test_async_frames_lf_bytes_and_preserves_split_utf8_and_json_line_separator(raw):
    responses = []
    first = dict(ITEM, custom_id="café\u2028東京", data=[{"embedding": [0.125, -0.5]}])
    second = dict(ITEM, task_id="task-2", custom_id="second")
    payload = (
        json.dumps(first, ensure_ascii=False).encode("utf-8")
        + b"\r\n\r\n"
        + json.dumps(second, ensure_ascii=False).encode("utf-8")
    )
    async with httpx.AsyncClient(transport=chunked_transport(payload, responses)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        items = await read_results_async(client, raw)

    assert [item.custom_id for item in items] == ["café\u2028東京", "second"]
    assert items[0].data[0].embedding == [0.125, -0.5]
    assert responses[0].is_closed


@pytest.mark.asyncio
@pytest.mark.parametrize("raw", [False, True])
@pytest.mark.parametrize(
    "payload",
    [
        b'{"task_id":"task-1","custom_id":"bad\xffid","status":"ready","data":[]}\n',
        b'{"task_id":"task-1","custom_id":"caf\xc3',
    ],
)
async def test_async_rejects_malformed_or_truncated_utf8_and_closes_response(raw, payload):
    responses = []
    streams = []
    if payload.endswith(b"\n"):
        payload += json.dumps(ITEM).encode() + b"\n"
    async with httpx.AsyncClient(
        transport=chunked_transport(
            payload, responses, TrackingResponse, StopAfterFirstLineStream, streams
        )
    ) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        with pytest.raises(UnicodeDecodeError):
            await read_results_async(client, raw)

    assert responses[0].is_closed
    assert typing.cast(TrackingResponse, responses[0]).byte_iterator_closed
    assert not streams[0].read_after_line


@pytest.mark.asyncio
@pytest.mark.parametrize("raw", [False, True])
async def test_async_malformed_utf8_closes_uninstrumented_httpx_iterator(raw):
    responses = []
    streams = []
    payload = (
        b'{"task_id":"task-1","custom_id":"bad\xffid","status":"ready","data":[]}\n'
        + json.dumps(ITEM).encode()
        + b"\n"
    )
    async with httpx.AsyncClient(
        transport=chunked_transport(payload, responses, stream_class=StopAfterFirstLineStream, streams=streams)
    ) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        with pytest.raises(UnicodeDecodeError):
            await read_results_async(client, raw)

    assert responses[0].is_closed
    assert not streams[0].read_after_line


@pytest.mark.parametrize("raw", [False, True])
def test_sync_closes_byte_iterator_when_consumer_stops_early(raw):
    responses = []
    streams = []
    payload = (json.dumps(ITEM) + "\n" + json.dumps(dict(ITEM, custom_id="second")) + "\n").encode()
    with httpx.Client(
        transport=chunked_transport(payload, responses, TrackingResponse, StopAfterFirstLineStream, streams)
    ) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        if raw:
            with client.embed.v_2.batches.with_raw_response.results(BATCH_ID) as response:
                next(response.data)
        else:
            results = typing.cast(
                typing.Generator[typing.Any, None, None], client.embed.v_2.batches.results(BATCH_ID)
            )
            next(results)
            results.close()

    assert responses[0].is_closed
    assert typing.cast(TrackingResponse, responses[0]).byte_iterator_closed
    assert not streams[0].read_after_line


@pytest.mark.asyncio
@pytest.mark.parametrize("raw", [False, True])
async def test_async_closes_byte_iterator_when_consumer_stops_early(raw):
    responses = []
    streams = []
    payload = (json.dumps(ITEM) + "\n" + json.dumps(dict(ITEM, custom_id="second")) + "\n").encode()
    async with httpx.AsyncClient(
        transport=chunked_transport(payload, responses, TrackingResponse, StopAfterFirstLineStream, streams)
    ) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        if raw:
            async with client.embed.v_2.batches.with_raw_response.results(BATCH_ID) as response:
                await response.data.__anext__()
        else:
            results = typing.cast(
                typing.AsyncGenerator[typing.Any, None], client.embed.v_2.batches.results(BATCH_ID)
            )
            await results.__anext__()
            await results.aclose()

    assert responses[0].is_closed
    assert typing.cast(TrackingResponse, responses[0]).byte_iterator_closed
    assert not streams[0].read_after_line
