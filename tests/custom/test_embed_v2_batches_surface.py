import json

import httpx
import pytest

from twelvelabs import (
    AsyncTwelveLabs,
    EmbeddingBatchImageInputRequest,
    EmbeddingBatchImageItemRequest,
    MediaSource,
    TwelveLabs,
)

BASE_URL = "https://api.example.com/v1.3"
BATCH_ID = "batch-123"
ITEM = {"task_id": "task-123", "custom_id": "image-001", "status": "ready", "data": []}
BATCH_ITEM = {"task_id": "task-123", "custom_id": "image-001", "status": "queued"}
OPERATIONS = [
    ("create", "POST", "/v1.3/embed-v2/batches"),
    ("list", "GET", "/v1.3/embed-v2/batches"),
    ("retrieve", "GET", f"/v1.3/embed-v2/batches/{BATCH_ID}"),
    ("results", "GET", f"/v1.3/embed-v2/batches/{BATCH_ID}/results"),
    ("cancel", "POST", f"/v1.3/embed-v2/batches/{BATCH_ID}/cancel"),
    ("delete", "DELETE", f"/v1.3/embed-v2/batches/{BATCH_ID}"),
]


def _batch_body(status="pending"):
    return {
        "batch_id": BATCH_ID,
        "client_batch_id": "client-batch-123",
        "model_name": "marengo3.5",
        "service_tier": "flex",
        "input_type": "image",
        "status": status,
        "total_items": 1,
        "queued_items": 1,
        "processing_items": 0,
        "ready_items": 0,
        "failed_items": 0,
        "canceled_items": 0,
        "created_at": "2026-10-28T00:00:00Z",
        "expires_at": "2026-10-29T00:00:00Z",
        "items": [BATCH_ITEM],
    }


def _batch_transport(requests):
    def handle(request):
        requests.append(request)
        if request.url.path.endswith("/results"):
            return httpx.Response(
                200,
                content=(json.dumps(ITEM) + "\n").encode(),
                headers={"content-type": "application/jsonl"},
            )
        if request.method == "DELETE":
            return httpx.Response(204)
        if request.url.path == "/v1.3/embed-v2/batches" and request.method == "GET":
            summary = _batch_body()
            summary.pop("items")
            return httpx.Response(
                200,
                json={
                    "data": [summary],
                    "page_info": {"page": 2, "limit_per_page": 4, "total_page": 2, "total_results": 1},
                },
            )
        status = "canceling" if request.url.path.endswith("/cancel") else "pending"
        return httpx.Response(200, json=_batch_body(status))

    return httpx.MockTransport(handle)


def _run_sync(client, operation):
    batches = client.embed.v_2.batches
    if operation == "create":
        return batches.create(
            model_name="marengo3.5",
            service_tier="flex",
            input_type="image",
            client_batch_id="client-batch-123",
            requests=[
                EmbeddingBatchImageItemRequest(
                    custom_id="image-001",
                    image=EmbeddingBatchImageInputRequest(
                        media_source=MediaSource(url="https://example.com/image.png")
                    ),
                )
            ],
        )
    if operation == "list":
        return batches.list(client_batch_id="client-batch-123", status="pending", page=2, page_limit=4)
    if operation == "retrieve":
        return batches.retrieve(BATCH_ID)
    if operation == "results":
        return list(batches.results(BATCH_ID))
    if operation == "cancel":
        return batches.cancel(BATCH_ID)
    return batches.delete(BATCH_ID)


async def _run_async(client, operation):
    batches = client.embed.v_2.batches
    if operation == "create":
        return await batches.create(
            model_name="marengo3.5",
            service_tier="flex",
            input_type="image",
            client_batch_id="client-batch-123",
            requests=[
                EmbeddingBatchImageItemRequest(
                    custom_id="image-001",
                    image=EmbeddingBatchImageInputRequest(
                        media_source=MediaSource(url="https://example.com/image.png")
                    ),
                )
            ],
        )
    if operation == "list":
        return await batches.list(client_batch_id="client-batch-123", status="pending", page=2, page_limit=4)
    if operation == "retrieve":
        return await batches.retrieve(BATCH_ID)
    if operation == "results":
        return [item async for item in batches.results(BATCH_ID)]
    if operation == "cancel":
        return await batches.cancel(BATCH_ID)
    return await batches.delete(BATCH_ID)


def _assert_result(operation, result):
    if operation == "create":
        assert result.batch_id == BATCH_ID
    elif operation == "list":
        assert [item.batch_id for item in result.data] == [BATCH_ID]
    elif operation == "retrieve":
        assert result.batch_id == BATCH_ID
    elif operation == "results":
        assert [item.custom_id for item in result] == ["image-001"]
    elif operation == "cancel":
        assert result.status == "canceling"
    else:
        assert result is None


def _assert_request(operation, request, expected_method, expected_path):
    assert request.method == expected_method
    assert request.url.path == expected_path
    if operation == "create":
        body = json.loads(request.content)
        assert body["model_name"] == "marengo3.5"
        assert body["service_tier"] == "flex"
        assert body["input_type"] == "image"
        assert body["client_batch_id"] == "client-batch-123"
        assert body["requests"][0]["custom_id"] == "image-001"
        assert body["requests"][0]["image"]["media_source"]["url"] == "https://example.com/image.png"
    elif operation == "list":
        assert dict(request.url.params) == {
            "client_batch_id": "client-batch-123",
            "status": "pending",
            "page": "2",
            "page_limit": "4",
        }
    else:
        assert request.content == b""


@pytest.mark.parametrize(("operation", "method", "path"), OPERATIONS)
def test_sync_public_embed_v2_batch_methods_dispatch_to_documented_routes(operation, method, path):
    requests = []
    with httpx.Client(transport=_batch_transport(requests)) as http:
        client = TwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        result = _run_sync(client, operation)

    assert len(requests) == 1
    _assert_result(operation, result)
    _assert_request(operation, requests[0], method, path)


@pytest.mark.asyncio
@pytest.mark.parametrize(("operation", "method", "path"), OPERATIONS)
async def test_async_public_embed_v2_batch_methods_dispatch_to_documented_routes(operation, method, path):
    requests = []
    async with httpx.AsyncClient(transport=_batch_transport(requests)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        result = await _run_async(client, operation)

    assert len(requests) == 1
    _assert_result(operation, result)
    _assert_request(operation, requests[0], method, path)
