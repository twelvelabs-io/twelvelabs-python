import json

import httpx
import pytest

from twelvelabs import AsyncTwelveLabs, TwelveLabs
from twelvelabs.errors import ForbiddenError, NotFoundError

BASE_URL = "https://api.example.com/v1.3"
TASK_ID = "task-123"
REQUEST_ID = "request-embed-v2-1"


def test_legacy_task_error_imports_remain_compatible():
    from twelvelabs import EmbeddingTaskError, EmbeddingTaskResponseError
    from twelvelabs.types import EmbeddingTaskResponseError as ErrorFromTypes
    from twelvelabs.types.embedding_task_response_error import EmbeddingTaskResponseError as ErrorFromModule

    assert EmbeddingTaskResponseError is EmbeddingTaskError
    assert ErrorFromTypes is EmbeddingTaskError
    assert ErrorFromModule is EmbeddingTaskError
    error = EmbeddingTaskResponseError(message="The embedding task failed.")
    assert isinstance(error, EmbeddingTaskError)
    assert error.message == "The embedding task failed."


def _transport(body, *, status_code=200, headers=None, requests=None):
    def handle(request):
        if requests is not None:
            requests.append(request)
        return httpx.Response(status_code, json=body, headers=headers)

    return httpx.MockTransport(handle)


def test_sync_embed_v2_task_create_accepts_queued_response():
    requests = []
    response_body = {"_id": TASK_ID, "status": "queued"}
    transport = _transport(response_body, requests=requests)

    with httpx.Client(transport=transport) as http:
        client = TwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        task = client.embed.v_2.tasks.create(
            input_type="audio",
            model_name="marengo3.5",
            audio={"media_source": {"url": "https://example.com/audio.wav"}},
        )

    assert task.id == TASK_ID
    assert task.status == "queued"
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST"
    assert request.url.path == "/v1.3/embed-v2/tasks"
    assert request.headers["x-api-key"] == "test-key"
    body = json.loads(request.content)
    assert body["input_type"] == "audio"
    assert body["model_name"] == "marengo3.5"
    assert body["audio"]["media_source"]["url"] == "https://example.com/audio.wav"


@pytest.mark.asyncio
async def test_async_embed_v2_task_create_accepts_queued_response():
    requests = []
    response_body = {"_id": TASK_ID, "status": "queued"}
    transport = _transport(response_body, requests=requests)

    async with httpx.AsyncClient(transport=transport) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        task = await client.embed.v_2.tasks.create(
            input_type="audio",
            model_name="marengo3.5",
            audio={"media_source": {"url": "https://example.com/audio.wav"}},
        )

    assert task.id == TASK_ID
    assert task.status == "queued"
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST"
    assert request.url.path == "/v1.3/embed-v2/tasks"
    assert request.headers["x-api-key"] == "test-key"
    body = json.loads(request.content)
    assert body["input_type"] == "audio"
    assert body["model_name"] == "marengo3.5"
    assert body["audio"]["media_source"]["url"] == "https://example.com/audio.wav"


def test_sync_embed_v2_task_cancel_uses_task_resource():
    requests = []
    response_body = {"_id": TASK_ID, "status": "canceled", "cancellation_reason": "user_requested"}

    with httpx.Client(transport=_transport(response_body, requests=requests)) as http:
        client = TwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        task = client.embed.v_2.tasks.cancel(TASK_ID)

    assert task.id == TASK_ID
    assert task.status == "canceled"
    assert task.cancellation_reason == "user_requested"
    assert len(requests) == 1
    assert requests[0].method == "POST"
    assert requests[0].url.path == f"/v1.3/embed-v2/tasks/{TASK_ID}/cancel"


@pytest.mark.asyncio
async def test_async_embed_v2_task_cancel_uses_task_resource():
    requests = []
    response_body = {"_id": TASK_ID, "status": "canceled", "cancellation_reason": "user_requested"}

    async with httpx.AsyncClient(transport=_transport(response_body, requests=requests)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        task = await client.embed.v_2.tasks.cancel(TASK_ID)

    assert task.id == TASK_ID
    assert task.status == "canceled"
    assert task.cancellation_reason == "user_requested"
    assert len(requests) == 1
    assert requests[0].method == "POST"
    assert requests[0].url.path == f"/v1.3/embed-v2/tasks/{TASK_ID}/cancel"


def test_sync_embed_v2_retrieve_preserves_future_status_and_fractional_duration():
    response_body = {
        "_id": TASK_ID,
        "status": "future_worker_state",
        "metadata": {
            "input_type": "audio",
            "duration": 1.25,
            "embedding_options": ["audio"],
            "embedding_scopes": ["clip"],
        },
    }
    requests = []

    with httpx.Client(transport=_transport(response_body, requests=requests)) as http:
        client = TwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        task = client.embed.v_2.tasks.retrieve(TASK_ID)

    assert task.status == "future_worker_state"
    assert task.metadata.duration == 1.25
    assert isinstance(task.metadata.duration, float)
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == f"/v1.3/embed-v2/tasks/{TASK_ID}"


@pytest.mark.asyncio
async def test_async_embed_v2_retrieve_preserves_future_status_and_fractional_duration():
    response_body = {
        "_id": TASK_ID,
        "status": "future_worker_state",
        "metadata": {
            "input_type": "audio",
            "duration": 1.25,
            "embedding_options": ["audio"],
            "embedding_scopes": ["clip"],
        },
    }
    requests = []

    async with httpx.AsyncClient(transport=_transport(response_body, requests=requests)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        task = await client.embed.v_2.tasks.retrieve(TASK_ID)

    assert task.status == "future_worker_state"
    assert task.metadata.duration == 1.25
    assert isinstance(task.metadata.duration, float)
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == f"/v1.3/embed-v2/tasks/{TASK_ID}"


def test_sync_embed_v2_retrieve_error_preserves_flat_body_and_headers():
    error_body = {"code": "task_not_found", "message": "Embedding task was not found"}
    headers = {"x-request-id": REQUEST_ID}

    with httpx.Client(transport=_transport(error_body, status_code=404, headers=headers)) as http:
        client = TwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        with pytest.raises(NotFoundError) as exc:
            client.embed.v_2.tasks.retrieve(TASK_ID)

    assert exc.value.status_code == 404
    assert exc.value.body == error_body
    assert exc.value.headers["x-request-id"] == REQUEST_ID


LEGACY_FORBIDDEN_BODY = {
    "code": "read_not_allowed",
    "message": "Task is outside the account.",
}


@pytest.mark.parametrize(
    ("operation", "expected_method", "expected_path"),
    [
        ("retrieve", "GET", f"/v1.3/embed-v2/tasks/{TASK_ID}"),
        ("cancel", "POST", f"/v1.3/embed-v2/tasks/{TASK_ID}/cancel"),
    ],
)
def test_sync_embed_v2_task_operations_preserve_legacy_forbidden_error(
    operation, expected_method, expected_path
):
    requests = []

    with httpx.Client(
        transport=_transport(LEGACY_FORBIDDEN_BODY, status_code=403, requests=requests)
    ) as http:
        client = TwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        with pytest.raises(ForbiddenError) as exc:
            getattr(client.embed.v_2.tasks, operation)(TASK_ID)

    assert exc.value.status_code == 403
    assert exc.value.body == LEGACY_FORBIDDEN_BODY
    assert len(requests) == 1
    assert requests[0].method == expected_method
    assert requests[0].url.path == expected_path


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("operation", "expected_method", "expected_path"),
    [
        ("retrieve", "GET", f"/v1.3/embed-v2/tasks/{TASK_ID}"),
        ("cancel", "POST", f"/v1.3/embed-v2/tasks/{TASK_ID}/cancel"),
    ],
)
async def test_async_embed_v2_task_operations_preserve_legacy_forbidden_error(
    operation, expected_method, expected_path
):
    requests = []

    async with httpx.AsyncClient(
        transport=_transport(LEGACY_FORBIDDEN_BODY, status_code=403, requests=requests)
    ) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        with pytest.raises(ForbiddenError) as exc:
            await getattr(client.embed.v_2.tasks, operation)(TASK_ID)

    assert exc.value.status_code == 403
    assert exc.value.body == LEGACY_FORBIDDEN_BODY
    assert len(requests) == 1
    assert requests[0].method == expected_method
    assert requests[0].url.path == expected_path


@pytest.mark.asyncio
async def test_async_embed_v2_retrieve_error_preserves_flat_body_and_headers():
    error_body = {"code": "task_not_found", "message": "Embedding task was not found"}
    headers = {"x-request-id": REQUEST_ID}

    async with httpx.AsyncClient(
        transport=_transport(error_body, status_code=404, headers=headers)
    ) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url=BASE_URL, httpx_client=http)
        with pytest.raises(NotFoundError) as exc:
            await client.embed.v_2.tasks.retrieve(TASK_ID)

    assert exc.value.status_code == 404
    assert exc.value.body == error_body
    assert exc.value.headers["x-request-id"] == REQUEST_ID
