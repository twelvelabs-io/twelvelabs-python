import json

import httpx
import pytest

from twelvelabs import AsyncTwelveLabs, TwelveLabs
from twelvelabs.types.audio_segmentation_fixed import AudioSegmentationFixed
from twelvelabs.types.temporal_segmentation_dynamic_dynamic import TemporalSegmentationDynamicDynamic
from twelvelabs.types.temporal_segmentation_fixed_fixed import TemporalSegmentationFixedFixed


@pytest.mark.parametrize(
    "model,field",
    [
        (AudioSegmentationFixed, "duration_sec"),
        (TemporalSegmentationFixedFixed, "duration_sec"),
        (TemporalSegmentationDynamicDynamic, "min_duration_sec"),
    ],
)
def test_fractional_segmentation_duration_is_not_rejected_or_truncated(model, field):
    value = model(**{field: 2.5})
    assert getattr(value, field) == 2.5


def _transport(requests):
    def handle(request):
        requests.append(json.loads(request.content))
        return httpx.Response(202, json={"_id": "task-1", "status": "queued"})

    return httpx.MockTransport(handle)


def test_sync_sends_fractional_duration():
    requests = []
    with httpx.Client(transport=_transport(requests)) as http:
        client = TwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        client.embed.v_2.tasks.create(
            model_name="marengo3.5",
            input_type="audio",
            audio={
                "media_source": {"url": "https://example.com/audio.wav"},
                "segmentation": {"strategy": "fixed", "fixed": AudioSegmentationFixed(duration_sec=2.5)},
            },
        )
    assert requests[0]["audio"]["segmentation"]["fixed"]["duration_sec"] == 2.5


@pytest.mark.asyncio
async def test_async_sends_fractional_duration():
    requests = []
    async with httpx.AsyncClient(transport=_transport(requests)) as http:
        client = AsyncTwelveLabs(api_key="test-key", base_url="https://api.example.com/v1.3", httpx_client=http)
        await client.embed.v_2.tasks.create(
            model_name="marengo3.5",
            input_type="audio",
            audio={
                "media_source": {"url": "https://example.com/audio.wav"},
                "segmentation": {"strategy": "fixed", "fixed": AudioSegmentationFixed(duration_sec=2.5)},
            },
        )
    assert requests[0]["audio"]["segmentation"]["fixed"]["duration_sec"] == 2.5
