"""Responses API examples over a knowledge store.

Covers:
  - non-streaming response
  - streaming response (SSE)
  - structured output (text.format = json_schema)
  - selections targeting a single item ({{sel:N}} tokens)
  - selections targeting an item collection
  - multi-turn conversation via session_id
  - include=["intermediate_outputs"]

Streaming uses responses.create_stream(), which returns an iterator of typed
ResponseStreamEvent objects (see `demo_streaming`).

Run:
    source env/bin/activate
    python examples/responses.py
"""

import json
import time
import uuid

from twelvelabs import (
    ResponseInputItem,
    ResponseSelection,
    TextParam,
)
from twelvelabs.core.api_error import ApiError
from twelvelabs.types.text_param_format import TextParamFormat_JsonSchema

from _ks_helpers import (
    cleanup_knowledge_store,
    make_client,
    setup_ready_knowledge_store,
)



def create_response(client, **kwargs):
    """Wrapper around responses.create that retries on HTTP 429.

    The /responses endpoint is rate-limited, so a script that fires several
    calls in a row may get a 429. This honors the `retry-after` header and retries.
    """
    while True:
        try:
            return client.responses.create(**kwargs)
        except ApiError as exc:
            if getattr(exc, "status_code", None) == 429:
                headers = getattr(exc, "headers", {}) or {}
                wait = int(headers.get("retry-after", "15")) + 1
                print(f"  [rate limited] waiting {wait}s then retrying ...")
                time.sleep(wait)
                continue
            raise


def print_response(resp, label):
    print(f"\n[{label}]")
    print(f"  id={resp.id} session_id={resp.session_id} status={resp.status}")
    if resp.usage is not None:
        print(f"  usage: input={resp.usage.input_tokens} output={resp.usage.output_tokens}")
    for item in resp.output or []:
        if item.content:
            for part in item.content:
                text = (part.text or "").strip()
                if text:
                    print(f"  [{item.type}] {text[:400]}")
        elif item.type == "function_call":
            print(f"  [function_call] name={item.name} args={item.arguments}")


def demo_non_streaming(client, ks_id):
    resp = create_response(
        client,
        knowledge_store_id=ks_id,
        input=[
            ResponseInputItem(
                type="message",
                role="user",
                content="Summarize what happens in this knowledge store in two sentences.",
            )
        ],
    )
    print_response(resp, "non-streaming")
    return resp.session_id


def demo_multi_turn(client, ks_id, session_id):
    """Continue the conversation started in demo_non_streaming."""
    if not session_id:
        print("\n[multi-turn] skipped (no session_id from previous turn)")
        return
    resp = create_response(
        client,
        knowledge_store_id=ks_id,
        session_id=session_id,
        input=[
            ResponseInputItem(
                type="message",
                role="user",
                content="Now list the three most important moments as bullet points.",
            )
        ],
    )
    print_response(resp, "multi-turn (same session)")


def demo_include_intermediate(client, ks_id):
    resp = create_response(
        client,
        knowledge_store_id=ks_id,
        input=[
            ResponseInputItem(
                type="message",
                role="user",
                content="What is the overall mood, and how did you decide?",
            )
        ],
        include=["intermediate_outputs"],
    )
    print_response(resp, "include=intermediate_outputs")


def demo_structured_output(client, ks_id):
    resp = create_response(
        client,
        knowledge_store_id=ks_id,
        input=[
            ResponseInputItem(
                type="message",
                role="user",
                content="Extract a title and a list of up to 3 tags for this content.",
            )
        ],
        text=TextParam(
            format=TextParamFormat_JsonSchema(
                name="content_summary",
                description="A short structured summary of the knowledge store content.",
                schema_={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "A short title."},
                        "tags": {
                            "type": "array",
                            "description": "Up to three descriptive tags.",
                            "items": {"type": "string", "description": "A single tag."},
                        },
                    },
                    "required": ["title", "tags"],
                    "additionalProperties": False,
                },
                strict=True,
            )
        ),
    )
    print_response(resp, "structured output (json_schema)")
    # The final message text should be a JSON string conforming to the schema.
    for item in resp.output or []:
        for part in item.content or []:
            if part.text:
                try:
                    parsed = json.loads(part.text)
                    print(f"  parsed JSON: {parsed}")
                except json.JSONDecodeError:
                    print("  (final text was not valid JSON)")


def demo_selections_item(client, ks_id, items):
    """Restrict the request to a single item and reference it with {{sel:0}}."""
    if "video" not in items:
        print("\n[selections:item] skipped (no video item)")
        return
    resp = create_response(
        client,
        knowledge_store_id=ks_id,
        input=[
            ResponseInputItem(
                type="message",
                role="user",
                content="Describe {{sel:0}} in one sentence.",
            )
        ],
        selections=[ResponseSelection(kind="item", id=items["video"])],
    )
    print_response(resp, "selections -> single item ({{sel:0}})")


def demo_selections_collection(client, ks_id, items):
    """Create a collection, then restrict a response to it via {{sel:0}}."""
    collection = client.knowledge_store_item_collections.create(
        knowledge_store_id=ks_id, name=f"resp-collection-{uuid.uuid4()}"
    )
    client.knowledge_store_item_collections.add_items(
        knowledge_store_id=ks_id, collection_id=collection.id, item_ids=list(items.values())
    )
    print(f"\n  created collection {collection.id} with {len(items)} item(s)")
    resp = create_response(
        client,
        knowledge_store_id=ks_id,
        input=[
            ResponseInputItem(
                type="message",
                role="user",
                content="Summarize the contents of {{sel:0}}.",
            )
        ],
        selections=[ResponseSelection(kind="collection", id=collection.id)],
    )
    print_response(resp, "selections -> collection ({{sel:0}})")
    client.knowledge_store_item_collections.delete(
        knowledge_store_id=ks_id, collection_id=collection.id
    )


def demo_streaming(client, ks_id):
    """Stream a response as Server-Sent Events via responses.create_stream(),
    which returns an iterator of typed ResponseStreamEvent objects.

    Assembles the incremental `response.output_text.delta` chunks into the final
    text as they arrive.
    """
    print("\n[streaming] responses.create_stream():")
    # create_stream() is lazy: the request fires when the iterator is first
    # consumed, not at the call, so the whole create+consume is wrapped in the retry.
    while True:
        try:
            text_parts = []
            event_count = 0
            for event in client.responses.create_stream(
                knowledge_store_id=ks_id,
                input=[
                    ResponseInputItem(
                        type="message",
                        role="user",
                        content="Give a one-sentence summary.",
                    )
                ],
            ):
                event_count += 1
                etype = getattr(event, "type", None)
                if etype == "response.output_text.delta":
                    text_parts.append(getattr(event, "delta", "") or "")
                elif etype == "response.completed":
                    print("  received response.completed")
            break
        except ApiError as exc:
            if getattr(exc, "status_code", None) == 429:
                wait = int((getattr(exc, "headers", {}) or {}).get("retry-after", "15")) + 1
                print(f"  [rate limited] waiting {wait}s then retrying ...")
                time.sleep(wait)
                continue
            raise
    print(f"  streamed {event_count} event(s)")
    print(f"  assembled text: {''.join(text_parts)[:400]}")


def main():
    with make_client() as client:
        # Create a knowledge store with a ready video and image item to reason over.
        setup = setup_ready_knowledge_store(
            client, name=f"ks-responses-{uuid.uuid4()}"
        )
        ks = setup.knowledge_store
        items = setup.items
        try:
            session_id = demo_non_streaming(client, ks.id)
            demo_multi_turn(client, ks.id, session_id)
            demo_include_intermediate(client, ks.id)
            demo_structured_output(client, ks.id)
            demo_selections_item(client, ks.id, items)
            demo_selections_collection(client, ks.id, items)
            demo_streaming(client, ks.id)
        finally:
            cleanup_knowledge_store(client, ks.id)


if __name__ == "__main__":
    main()
