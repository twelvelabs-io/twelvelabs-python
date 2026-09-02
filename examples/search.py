"""Search your content with Marengo 3.0.

An index makes your content searchable. Marengo 3.0 is the index model; Pegasus 1.5
analyzes video directly without an index, so see analyze.py for that.

The flow is: upload an asset, index it, then search.

Run:
    export API_KEY=...
    export INDEX_ID=...      # optional: reuse an index instead of creating one
    python examples/search.py
"""

import os
import time
import uuid

from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem

API_KEY = os.getenv("API_KEY") or os.getenv("TWELVE_LABS_API_KEY")
assert API_KEY, "Set your API key in the API_KEY environment variable."

INDEX_ID = os.getenv("INDEX_ID")
VIDEO_PATH = os.path.join(os.path.dirname(__file__), "assets/example.mp4")

with TwelveLabs(api_key=API_KEY) as client:
    if INDEX_ID:
        index = client.indexes.retrieve(index_id=INDEX_ID)
        print(f"Using index: id={index.id} name={index.index_name}")
    else:
        index = client.indexes.create(
            index_name=f"idx-{uuid.uuid4()}",
            models=[
                IndexesCreateRequestModelsItem(
                    model_name="marengo3.0", model_options=["visual", "audio"]
                ),
            ],
            addons=["thumbnail"],
        )
        print(f"Created index: id={index.id}")

        # Upload the video as an asset, then index that asset. See assets.py for
        # uploading from a URL and for large files.
        with open(VIDEO_PATH, "rb") as video_file:
            asset = client.assets.create(method="direct", file=video_file)
        while asset.status == "processing":
            time.sleep(5)
            asset = client.assets.retrieve(asset_id=asset.id)
        print(f"Uploaded asset: id={asset.id} status={asset.status}")

        indexed = client.indexes.indexed_assets.create(
            index_id=index.id, asset_id=asset.id
        )
        print(f"Indexing: indexed_asset_id={indexed.id}")

        # Indexing takes a few minutes. The asset is searchable once it is ready.
        detail = client.indexes.indexed_assets.retrieve(
            index_id=index.id, indexed_asset_id=indexed.id
        )
        while detail.status not in ("ready", "failed"):
            time.sleep(10)
            detail = client.indexes.indexed_assets.retrieve(
                index_id=index.id, indexed_asset_id=indexed.id
            )
            print(f"  status={detail.status}")
        if detail.status == "failed":
            raise SystemExit("indexing failed")

    # --- Search, grouped by video ------------------------------------------
    print("\nSearch (group by video):")
    for group in client.search.query(
        index_id=index.id,
        search_options=["visual", "audio"],
        query_text="A man talking",
        group_by="video",
    ):
        if group.clips is None:
            continue
        print(f"  video_id={group.id}")
        for clip in group.clips[:3]:
            print(f"    rank={clip.rank} start={clip.start} end={clip.end}")

    # --- Search, ungrouped clips -------------------------------------------
    print("\nSearch (no grouping):")
    for clip in list(
        client.search.query(
            index_id=index.id,
            search_options=["visual", "audio"],
            query_text="A man talking",
        )
    )[:5]:
        print(f"  video_id={clip.video_id} rank={clip.rank} start={clip.start} end={clip.end}")
