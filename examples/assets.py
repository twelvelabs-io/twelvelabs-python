"""Assets — the input path for analysis and embeddings.

Both Pegasus 1.5 analysis and Marengo 3.5 embeddings take an `asset_id`, so this is
where most workflows start. Covers direct upload (file and URL), polling for
readiness, listing, user metadata, transcription, and multipart upload for large
files.

Run:
    export API_KEY=...
    python examples/assets.py
"""

import itertools
import json
import os
import time

from twelvelabs import TwelveLabs

API_KEY = os.getenv("API_KEY") or os.getenv("TWELVE_LABS_API_KEY")
assert API_KEY, "Set your API key in the API_KEY environment variable."

HERE = os.path.dirname(__file__)
VIDEO_PATH = os.path.join(HERE, "assets/example.mp4")
IMAGE_URL = "https://www.gstatic.com/webp/gallery/1.jpg"


def wait_until_ready(client: TwelveLabs, asset_id: str, timeout_sec: int = 600):
    """An asset must be `ready` before analyze or embed will accept it."""
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        asset = client.assets.retrieve(asset_id=asset_id)
        if asset.status != "processing":
            return asset
        time.sleep(5)
    raise TimeoutError(f"asset {asset_id} still processing after {timeout_sec}s")


with TwelveLabs(api_key=API_KEY) as client:
    # --- Upload a local file ------------------------------------------------
    # `enable_hls` gives you a playable manifest; `enable_thumbnail` a poster frame.
    print("Upload from a local file:")
    with open(VIDEO_PATH, "rb") as video_file:
        video = client.assets.create(
            method="direct",
            file=video_file,
            enable_hls=True,
            enable_thumbnail=True,
            # user_metadata is a JSON-encoded string on this endpoint, not an object.
            user_metadata=json.dumps({"source": "examples", "kind": "demo"}),
        )
    print(f"  id={video.id} status={video.status} filename={video.filename}")
    video = wait_until_ready(client, video.id)
    print(f"  ready: file_type={video.file_type}")

    # --- Upload from a URL --------------------------------------------------
    # Use a direct link to a raw media file; sharing links are not supported.
    print("\nUpload from a URL:")
    image = client.assets.create(method="url", url=IMAGE_URL)
    image = wait_until_ready(client, image.id)
    print(f"  id={image.id} status={image.status} file_type={image.file_type}")

    # --- List ---------------------------------------------------------------
    # assets.list returns a pager that walks every page, so slice it rather than
    # calling list() on it.
    print("\nRecent assets:")
    for asset in itertools.islice(client.assets.list(page_limit=5), 5):
        print(f"  {asset.id} {asset.status:10} {asset.filename}")

    # --- User metadata ------------------------------------------------------
    # Attach your own fields, then filter or correlate on them later.
    print("\nUser metadata:")
    client.assets.update_user_metadata(
        asset_id=video.id, user_metadata={"source": "examples", "reviewed": True}
    )
    print(f"  {client.assets.retrieve(asset_id=video.id).user_metadata}")

    # --- Transcription ------------------------------------------------------
    # Available for assets with an audio track once processing finishes.
    # Transcription runs as its own job after the asset is ready, so poll for it.
    # `include` selects the granularity and defaults to `words`, so request
    # whichever ones you intend to read. Utterances add a `speaker` field.
    print("\nTranscription:")
    transcription = client.assets.retrieve_transcription(
        asset_id=video.id, include=["sentences", "utterances"]
    )
    while transcription.status in ("pending", "processing"):
        time.sleep(5)
        transcription = client.assets.retrieve_transcription(
            asset_id=video.id, include=["sentences", "utterances"]
        )
    print(f"  status={transcription.status}")
    for sentence in (transcription.sentences or [])[:2]:
        print(f"    [{sentence.start}-{sentence.end}] {sentence.value}")
    for utterance in (transcription.utterances or [])[:2]:
        print(f"    speaker={utterance.speaker} [{utterance.start}] {utterance.value}")

    # --- Multipart upload ---------------------------------------------------
    # For large files. The wrapper handles chunking, retries and progress.
    print("\nMultipart upload:")
    large = client.multipart_upload.upload_file(
        file_path=VIDEO_PATH,
        filename="example-multipart.mp4",
    )
    print(f"  asset_id={large.asset_id if hasattr(large, 'asset_id') else large}")

    # --- Clean up -----------------------------------------------------------
    # `force=True` deletes even when the asset is referenced elsewhere.
    print("\nCleanup:")
    for asset_id in (image.id,):
        client.assets.delete(asset_id=asset_id, force=True)
        print(f"  deleted {asset_id}")
