import json

import httpx
import pytest

from twelvelabs import AsyncTwelveLabs, TwelveLabs

KNOWLEDGE_STORE_ID = "ks_019ebcf4-7e08-7201-b69c-69e0c1e6ae56"
INPUT = [{"type": "message", "role": "user", "content": "hello"}]
UNKNOWN_OUTPUT = {
    "type": "jockey:future_tool",
    "id": "item-unknown",
    "status": "completed",
    "future_payload": {"x": 1},
}


def response_payload(status="completed"):
    return {
        "id": "resp-test",
        "type": "response",
        "object": "response",
        "status": status,
        "output": [UNKNOWN_OUTPUT],
    }


def stream_payload(terminal_type, status):
    created = {
        "type": "response.created",
        "sequence_number": 0,
        "response": {
            "id": "resp-test",
            "type": "response",
            "object": "response",
            "status": "in_progress",
            "output": [],
        },
    }
    terminal = {
        "type": terminal_type,
        "sequence_number": 1,
        "response": response_payload(status),
    }
    return (
        "event: response.created\ndata: "
        + json.dumps(created)
        + "\n\nevent: "
        + terminal_type
        + "\ndata: "
        + json.dumps(terminal)
        + "\n\ndata: [DONE]\n\n"
    ).encode()


def transport(payload, responses):
    def handle(request):
        assert request.url.path == "/v1.3/responses"
        response = httpx.Response(
            200,
            stream=httpx.ByteStream(payload),
            headers={"content-type": "text/event-stream"},
        )
        responses.append(response)
        return response

    return httpx.MockTransport(handle)


def assert_unknown_output_item(item):
    assert item.type == "jockey:future_tool"
    assert item.id == "item-unknown"
    assert item.status == "completed"
    assert item.dict()["future_payload"] == {"x": 1}


@pytest.mark.parametrize("raw", [False, True])
def test_sync_create_preserves_unknown_output_item(raw):
    responses = []
    with httpx.Client(transport=transport(json.dumps(response_payload()).encode(), responses)) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        if raw:
            response = client.responses.with_raw_response.create(
                knowledge_store_id=KNOWLEDGE_STORE_ID,
                input=INPUT,
            )
            try:
                assert_unknown_output_item(response.data.output[0])
            finally:
                response.close()
        else:
            response = client.responses.create(knowledge_store_id=KNOWLEDGE_STORE_ID, input=INPUT)
            assert_unknown_output_item(response.output[0])

    assert responses[0].is_closed


@pytest.mark.parametrize("terminal_type,status", [("response.completed", "completed"), ("response.failed", "failed")])
@pytest.mark.parametrize("raw", [False, True])
def test_sync_create_stream_keeps_terminal_event_with_unknown_output_item(terminal_type, status, raw):
    responses = []
    with httpx.Client(transport=transport(stream_payload(terminal_type, status), responses)) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        if raw:
            with client.responses.with_raw_response.create_stream(
                knowledge_store_id=KNOWLEDGE_STORE_ID,
                input=INPUT,
            ) as response:
                events = list(response.data)
        else:
            events = list(client.responses.create_stream(knowledge_store_id=KNOWLEDGE_STORE_ID, input=INPUT))

    assert [event.type for event in events] == ["response.created", terminal_type]
    assert_unknown_output_item(events[-1].response.output[0])
    assert responses[0].is_closed


@pytest.mark.asyncio
@pytest.mark.parametrize("raw", [False, True])
async def test_async_create_preserves_unknown_output_item(raw):
    responses = []
    async with httpx.AsyncClient(transport=transport(json.dumps(response_payload()).encode(), responses)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        if raw:
            response = await client.responses.with_raw_response.create(
                knowledge_store_id=KNOWLEDGE_STORE_ID,
                input=INPUT,
            )
            try:
                assert_unknown_output_item(response.data.output[0])
            finally:
                await response.close()
        else:
            response = await client.responses.create(knowledge_store_id=KNOWLEDGE_STORE_ID, input=INPUT)
            assert_unknown_output_item(response.output[0])

    assert responses[0].is_closed


@pytest.mark.asyncio
@pytest.mark.parametrize("terminal_type,status", [("response.completed", "completed"), ("response.failed", "failed")])
@pytest.mark.parametrize("raw", [False, True])
async def test_async_create_stream_keeps_terminal_event_with_unknown_output_item(terminal_type, status, raw):
    responses = []
    async with httpx.AsyncClient(transport=transport(stream_payload(terminal_type, status), responses)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        if raw:
            async with client.responses.with_raw_response.create_stream(
                knowledge_store_id=KNOWLEDGE_STORE_ID,
                input=INPUT,
            ) as response:
                events = [event async for event in response.data]
        else:
            events = [
                event
                async for event in client.responses.create_stream(
                    knowledge_store_id=KNOWLEDGE_STORE_ID,
                    input=INPUT,
                )
            ]

    assert [event.type for event in events] == ["response.created", terminal_type]
    assert_unknown_output_item(events[-1].response.output[0])
    assert responses[0].is_closed
