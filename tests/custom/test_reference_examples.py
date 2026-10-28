from pathlib import Path

from scripts.normalize_reference import (
    PublicClientResolver,
    _fenced_python_blocks,
    normalize_reference,
)

SDK_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_PATH = SDK_ROOT / "reference.md"


def test_generated_reference_is_normalized_and_idempotent():
    reference = REFERENCE_PATH.read_text(encoding="utf-8")
    resolver = PublicClientResolver()
    try:
        normalized, changes = normalize_reference(reference, resolver)
        assert changes == 0
        assert normalized == reference
        for block in _fenced_python_blocks(reference):
            compile(block.source, "reference.md:{}".format(block.opening_line), "exec")
        assert resolver.requests == []
    finally:
        resolver.close()


def test_normalizes_public_iterators_and_preserves_raw_and_model_data():
    fixture = '''```python
from twelvelabs import TwelveLabs

client = TwelveLabs(api_key="test")
response = client.embed.v_2.batches.results(batch_id="batch-id")
for chunk in response.data:
    yield chunk
```

```python
from twelvelabs import TwelveLabs

def raw_example():
    client = TwelveLabs(api_key="test")
    response = client.with_raw_response.embed.v_2.batches.results(batch_id="batch-id")
    for chunk in response.data:
        yield chunk
```

```python
from twelvelabs import TwelveLabs

def model_example():
    client = TwelveLabs(api_key="test")
    response = client.embed.v_2.batches.list()
    for batch in response.data:
        yield batch
```

```python
from twelvelabs import TwelveLabs

def rebound_client_example():
    client = TwelveLabs(api_key="test")
    client = object()
    response = client.embed.v_2.batches.results(batch_id="batch-id")
    for chunk in response.data:
        yield chunk
```

```python
from twelvelabs import AsyncTwelveLabs

async def async_example():
    client = AsyncTwelveLabs(api_key="test")
    response = client.embed.v_2.batches.results(batch_id="batch-id")
    async for chunk in response.data:
        yield chunk
```
'''
    resolver = PublicClientResolver()
    try:
        normalized, changes = normalize_reference(fixture, resolver)
        normalized_again, second_changes = normalize_reference(normalized, resolver)
        assert changes == 2
        assert second_changes == 0
        assert normalized_again == normalized
        assert "for chunk in response:\n    print(chunk)" in normalized
        assert "client.with_raw_response.embed.v_2.batches.results" in normalized
        assert "for chunk in response.data" in normalized
        assert "for batch in response.data" in normalized
        assert "client = object()" in normalized
        assert "async for chunk in response:" in normalized
        assert "async for chunk in response.data" not in normalized
        assert "async for chunk in response:\n        yield chunk" in normalized
        for block in _fenced_python_blocks(normalized):
            compile(block.source, "<reference-fixture>", "exec")
        assert resolver.requests == []
    finally:
        resolver.close()
