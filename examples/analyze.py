"""Pegasus 1.5 analysis — synchronous and streaming.

Run:
    export API_KEY=...
    export ASSET_ID=...
    python examples/analyze.py
"""

import os

from twelvelabs import TwelveLabs, VideoContext_AssetId
from twelvelabs.types import StreamAnalyzeResponse_StreamEnd

API_KEY = os.getenv("API_KEY") or os.getenv("TWELVE_LABS_API_KEY")
assert API_KEY, "Set your API key in the API_KEY environment variable."

ASSET_ID = os.getenv("ASSET_ID", "<YOUR_ASSET_ID>")

with TwelveLabs(api_key=API_KEY) as client:
    # `video` is a discriminated union — the `type` field is required. The
    # VideoContext_* constructors set it for you; a plain {"asset_id": ...} dict
    # omits it and the request fails.
    video = VideoContext_AssetId(asset_id=ASSET_ID)
    # Also available: VideoContext_Url(url=...), VideoContext_Base64String(...)

    # --- Analyze ------------------------------------------------------------
    print("Analysis:")
    res = client.analyze(
        model_name="pegasus1.5",
        video=video,
        prompt="Describe this video in one sentence.",
    )
    print(f"  {res.data}")
    print(f"  usage={res.usage}")

    # --- Stream the same analysis -------------------------------------------
    print("\nStreaming:")
    for chunk in client.analyze_stream(
        model_name="pegasus1.5",
        video=video,
        prompt="List three facts about this video.",
    ):
        if chunk.event_type == "text_generation":
            print(chunk.text, end="", flush=True)
        elif isinstance(chunk, StreamAnalyzeResponse_StreamEnd):
            print(f"\n  finish_reason={chunk.finish_reason}")
