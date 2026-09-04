"""Pegasus 1.5 asynchronous analysis and video segmentation.

Use the async endpoint for long videos or when you do not want to hold a connection
open. Segmentation (`analysis_mode="time_based_metadata"`) is async only.

Run:
    export API_KEY=...
    export ASSET_ID=...
    python examples/analyze_async.py
"""

import json
import os
import time

from twelvelabs import TwelveLabs, VideoContext_AssetId
from twelvelabs.types import AsyncResponseFormat

API_KEY = os.getenv("API_KEY") or os.getenv("TWELVE_LABS_API_KEY")
assert API_KEY, "Set your API key in the API_KEY environment variable."

ASSET_ID = os.getenv("ASSET_ID", "<YOUR_ASSET_ID>")
MODEL = "pegasus1.5"


# A task is done once it leaves these states.
IN_FLIGHT = ("queued", "pending", "processing")


def wait_for(client: TwelveLabs, task_id: str, timeout_sec: int = 900):
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        task = client.analyze_async.tasks.retrieve(task_id)
        if task.status not in IN_FLIGHT:
            return task
        time.sleep(5)
    raise TimeoutError(f"task {task_id} did not finish in {timeout_sec}s")


with TwelveLabs(api_key=API_KEY) as client:
    video = VideoContext_AssetId(asset_id=ASSET_ID)

    # --- Async analysis -----------------------------------------------------
    # `custom_id` is echoed back so you can correlate results with your own records.
    # Async analysis takes max_tokens from 512 upward; the sync endpoint allows 1-4096.
    print("Async analysis:")
    task = client.analyze_async.tasks.create(
        video=video,
        model_name=MODEL,
        analysis_mode="general",
        prompt="Summarize this video in three sentences.",
        custom_id="example-general-1",
        max_tokens=1024,
    )
    done = wait_for(client, task.task_id)
    print(f"  status={done.status} custom_id={done.custom_id}")
    if done.result:
        print(f"  {done.result.data}")

    # --- Video segmentation -------------------------------------------------
    # Define the segments you want and the fields to extract for each one. The
    # platform returns timestamped segments carrying those fields.
    print("\nSegmentation:")
    task = client.analyze_async.tasks.create(
        video=video,
        model_name=MODEL,
        analysis_mode="time_based_metadata",
        response_format=AsyncResponseFormat(
            type="segment_definitions",
            segment_definitions=[
                {
                    "id": "scene",
                    "description": "A distinct scene or setting change in the video",
                    "fields": [
                        {
                            "name": "sentiment",
                            "type": "string",
                            "description": "The emotional tone of this segment",
                            "enum": ["positive", "negative", "neutral"],
                        }
                    ],
                }
            ],
        ),
        min_segment_duration=5.0,
    )
    done = wait_for(client, task.task_id)
    print(f"  status={done.status}")
    if done.result:
        # result.data is a JSON-encoded string keyed by segment definition id.
        for definition_id, segments in json.loads(done.result.data).items():
            print(f"  '{definition_id}': {len(segments)} segments")
            for seg in segments[:3]:
                print(f"    {json.dumps(seg)}")
