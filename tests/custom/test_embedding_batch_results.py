import json

import httpx
import pydantic
import pytest

from twelvelabs import AsyncTwelveLabs, TwelveLabs
from twelvelabs.errors import NotFoundError

BATCH_ID = "68d3ae81c4a8d3697e15b2ef"
ITEM = {"task_id": "task-1", "custom_id": "first", "status": "ready", "data": []}


def read_results(client, raw):
    if raw:
        with client.create_embeddings.with_raw_response.retrieve_embedding_batch_results(BATCH_ID) as response:
            assert response.headers["x-request-id"] == "request-1"
            return list(response.data)
    return list(client.create_embeddings.retrieve_embedding_batch_results(BATCH_ID))


async def read_results_async(client, raw):
    if raw:
        async with client.create_embeddings.with_raw_response.retrieve_embedding_batch_results(BATCH_ID) as response:
            assert response.headers["x-request-id"] == "request-1"
            return [item async for item in response.data]
    return [item async for item in client.create_embeddings.retrieve_embedding_batch_results(BATCH_ID)]


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
