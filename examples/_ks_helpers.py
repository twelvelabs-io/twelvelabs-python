"""Shared helpers for the knowledge-store and responses examples.

These utilities create assets, spin up a knowledge store, add items, and poll
until everything is ready so the search / responses examples have real content
to run against. Import them from `knowledge_stores.py` and `responses.py`, or
reuse them in your own scripts.

Environment:
    API_KEY               (required) your TwelveLabs API key
    TWELVELABS_BASE_URL   (optional) override the API base URL. When unset the
                          SDK default (prod, https://api.twelvelabs.io/v1.3) is used.
"""

import os
import time
import uuid
from typing import Dict, NamedTuple, Optional

from twelvelabs import TwelveLabs
from twelvelabs.types import AssetDetail, KnowledgeStore


class KnowledgeStoreSetup(NamedTuple):
    knowledge_store: KnowledgeStore
    items: Dict[str, str]  # {"video": item_id, "image": item_id}

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
VIDEO_PATH = os.path.join(ASSETS_DIR, "example.mp4")
IMAGE_PATH = os.path.join(ASSETS_DIR, "search_sample.png")

# A small, reliably-reachable public sample used for the `method="url"` path.
PUBLIC_VIDEO_URL = (
    "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
)


def make_client() -> TwelveLabs:
    """Build a client from API_KEY (+ optional TWELVELABS_BASE_URL)."""
    api_key = os.getenv("API_KEY")
    assert api_key, "Set your API key in an environment variable named API_KEY."
    base_url = os.getenv("TWELVELABS_BASE_URL")
    if base_url:
        return TwelveLabs(api_key=api_key, base_url=base_url)
    return TwelveLabs(api_key=api_key)


def create_asset_from_file(client: TwelveLabs, path: str, **kwargs) -> str:
    """Upload a local file as an asset (method='direct'). Returns the asset id."""
    with open(path, "rb") as f:
        asset = client.assets.create(method="direct", file=f, **kwargs)
    print(f"  Created asset (direct): id={asset.id} from {os.path.basename(path)}")
    return asset.id


def create_asset_from_url(client: TwelveLabs, url: str, **kwargs) -> str:
    """Create an asset from a public URL (method='url'). Returns the asset id."""
    asset = client.assets.create(method="url", url=url, **kwargs)
    print(f"  Created asset (url): id={asset.id}")
    return asset.id


def wait_for_asset_ready(
    client: TwelveLabs, asset_id: str, timeout: float = 600, interval: float = 5
) -> AssetDetail:
    """Poll an asset until it reaches a terminal status (ready/failed)."""
    deadline = time.time() + timeout
    while True:
        asset = client.assets.retrieve(asset_id=asset_id)
        if asset.status in ("ready", "failed"):
            print(f"  Asset {asset_id} status={asset.status}")
            if asset.status == "failed":
                raise RuntimeError(f"Asset {asset_id} failed to process")
            return asset
        if time.time() > deadline:
            raise TimeoutError(f"Asset {asset_id} not ready after {timeout}s (status={asset.status})")
        print(f"  Asset {asset_id} status={asset.status} ... waiting")
        time.sleep(interval)


def wait_for_item_ready(
    client: TwelveLabs,
    knowledge_store_id: str,
    item_id: str,
    timeout: float = 900,
    interval: float = 10,
):
    """Poll a knowledge store item until it is ready (or fails / times out)."""
    deadline = time.time() + timeout
    while True:
        item = client.knowledge_store_items.retrieve(
            knowledge_store_id=knowledge_store_id, item_id=item_id
        )
        if item.status in ("ready", "failed"):
            print(f"  Item {item_id} status={item.status}")
            if item.status == "failed":
                raise RuntimeError(f"Item {item_id} failed to process")
            return item
        if time.time() > deadline:
            raise TimeoutError(f"Item {item_id} not ready after {timeout}s (status={item.status})")
        print(f"  Item {item_id} status={item.status} ... waiting")
        time.sleep(interval)


def setup_ready_knowledge_store(
    client: TwelveLabs,
    name: Optional[str] = None,
    ingestion_config=None,
    add_video: bool = True,
    add_image: bool = True,
    wait: bool = True,
) -> KnowledgeStoreSetup:
    """Create a knowledge store, add a video and/or image item, and (optionally)
    wait until the items are ready.

    Returns a KnowledgeStoreSetup(knowledge_store=..., items={"video": id, ...}).
    """
    name = name or f"ks-example-{uuid.uuid4()}"
    ks: KnowledgeStore = client.knowledge_stores.create(
        name=name, ingestion_config=ingestion_config
    )
    print(f"Created knowledge store: id={ks.id} name={ks.name}")

    items: Dict[str, str] = {}

    if add_video:
        video_asset_id = create_asset_from_file(client, VIDEO_PATH)
        wait_for_asset_ready(client, video_asset_id)
        video_item = client.knowledge_store_items.create(
            knowledge_store_id=ks.id, asset_id=video_asset_id, asset_type="video"
        )
        items["video"] = video_item.id
        print(f"  Added video item: id={video_item.id}")

    if add_image:
        image_asset_id = create_asset_from_file(client, IMAGE_PATH)
        wait_for_asset_ready(client, image_asset_id)
        image_item = client.knowledge_store_items.create(
            knowledge_store_id=ks.id, asset_id=image_asset_id, asset_type="image"
        )
        items["image"] = image_item.id
        print(f"  Added image item: id={image_item.id}")

    if wait:
        for kind, item_id in items.items():
            print(f"Waiting for {kind} item {item_id} to be ready ...")
            wait_for_item_ready(client, ks.id, item_id)

    return KnowledgeStoreSetup(knowledge_store=ks, items=items)


def cleanup_knowledge_store(client: TwelveLabs, knowledge_store_id: str) -> None:
    """Delete a knowledge store (and all its items). Best-effort."""
    try:
        client.knowledge_stores.delete(knowledge_store_id=knowledge_store_id)
        print(f"Deleted knowledge store {knowledge_store_id}")
    except Exception as exc:  # noqa: BLE001
        print(f"  (cleanup) failed to delete {knowledge_store_id}: {exc}")
