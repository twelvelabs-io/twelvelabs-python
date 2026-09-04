"""Marengo 3.5 embeddings — one example per modality.

Run:
    export API_KEY=...
    export VIDEO_ASSET_ID=... AUDIO_ASSET_ID=... PDF_ASSET_ID=...
    python examples/embed_v2.py
"""

import os
import time

from twelvelabs import (
    AsyncAudioInputRequest,
    AsyncDocumentInputRequest,
    AsyncTemporalSegmentation,
    AsyncVideoInputRequest,
    MediaSource,
    MultiInputRequest,
    TemporalSegmentation_Dynamic,
    TemporalSegmentationDynamicDynamic,
    TwelveLabs,
)

API_KEY = os.getenv("API_KEY") or os.getenv("TWELVE_LABS_API_KEY")
assert API_KEY, "Set your API key in the API_KEY environment variable."

VIDEO_ASSET_ID = os.getenv("VIDEO_ASSET_ID", "<YOUR_VIDEO_ASSET_ID>")
AUDIO_ASSET_ID = os.getenv("AUDIO_ASSET_ID", "<YOUR_AUDIO_ASSET_ID>")
PDF_ASSET_ID = os.getenv("PDF_ASSET_ID", "<YOUR_PDF_ASSET_ID>")

MODEL = "marengo3.5"

# Dynamic segmentation, shared by the video and audio examples.
SEGMENTATION = AsyncTemporalSegmentation(
    temporal=TemporalSegmentation_Dynamic(
        dynamic=TemporalSegmentationDynamicDynamic(min_duration_sec=3)
    )
)


def wait_for(client: TwelveLabs, task_id: str, timeout_sec: int = 600):
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        task = client.embed.v_2.tasks.retrieve(task_id)
        if task.status != "processing":
            return task
        time.sleep(5)
    raise TimeoutError(f"task {task_id} still processing after {timeout_sec}s")


def show(task):
    print(f"  status={task.status}")
    if task.status != "ready":
        print(f"  error={task.error.message if task.error else None}")
        return
    for item in (task.data or [])[:3]:
        print(
            f"    option={item.embedding_option} scope={item.embedding_scope} "
            f"dim={len(item.embedding or [])}"
        )


with TwelveLabs(api_key=API_KEY) as client:
    # --- Query embedding (synchronous) --------------------------------------
    # With Marengo 3.5 the sync endpoint takes `multi_input`. Use it for the query
    # side of a retrieval flow; embed your library asynchronously below.
    print("Text query:")
    res = client.embed.v_2.create(
        input_type="multi_input",
        model_name=MODEL,
        multi_input=MultiInputRequest(input_text="a man walking a dog on the beach"),
    )
    print(f"  dim={len(res.data[0].embedding)} usage={res.usage}")

    # --- Video --------------------------------------------------------------
    # `embedding_option` must be set explicitly: the default includes
    # `transcription`, which is Marengo 3.0 only.
    print("\nVideo:")
    task = client.embed.v_2.tasks.create(
        input_type="video",
        model_name=MODEL,
        video=AsyncVideoInputRequest(
            media_source=MediaSource(asset_id=VIDEO_ASSET_ID),
            segmentation=SEGMENTATION,
            embedding_option=["visual", "audio"],
            embedding_scope=["local"],
        ),
    )
    show(wait_for(client, task.id))

    # --- Audio --------------------------------------------------------------
    # On Marengo 3.5 the `audio` option covers speech, music and non-dialog audio.
    print("\nAudio:")
    task = client.embed.v_2.tasks.create(
        input_type="audio",
        model_name=MODEL,
        audio=AsyncAudioInputRequest(
            media_source=MediaSource(asset_id=AUDIO_ASSET_ID),
            segmentation=SEGMENTATION,
            embedding_option=["audio"],
            embedding_scope=["local"],
        ),
    )
    show(wait_for(client, task.id))

    # --- Document -----------------------------------------------------------
    # PDF pages are embedded as images, so the option is `visual` and `local`
    # yields one embedding per page. For plain text or Markdown, use
    # embedding_option=["text"] with embedding_scope=["asset"].
    print("\nDocument (PDF, one embedding per page):")
    task = client.embed.v_2.tasks.create(
        input_type="document",
        model_name=MODEL,
        document=AsyncDocumentInputRequest(
            media_source=MediaSource(asset_id=PDF_ASSET_ID),
            embedding_option=["visual"],
            embedding_scope=["local"],
        ),
    )
    show(wait_for(client, task.id))
