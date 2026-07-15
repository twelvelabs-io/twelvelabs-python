"""Knowledge store examples: assets, stores, items, item collections, and search.

Covers, end to end:
  - creating a knowledge store with each ingestion_config variant
    (none / description enrichment / json_schema enrichment)
  - knowledge store CRUD (create, retrieve, update, list, delete)
  - adding assets as items and polling until ready
  - listing / filtering items by status
  - item collections (create, add items, list, remove, update, delete)
  - search: default, group_by=item, asset_type filter, item_id filter,
    modality options, include_metadata, and pagination

Run:
    source env/bin/activate
    python examples/knowledge_stores.py
"""

import uuid

from twelvelabs import (
    AssetTypeFilter,
    EnrichmentConfig_Description,
    EnrichmentConfig_JsonSchema,
    EnrichmentConfigJsonSchemaJsonSchema,
    IngestionConfig,
    ItemIdFilter,
    KnowledgeStoreSearchQuery,
    SearchKnowledgeStoreFilter,
    SearchKnowledgeStoreOptions,
    VideoSearchOptions,
)

from _ks_helpers import (
    IMAGE_PATH,
    VIDEO_PATH,
    cleanup_knowledge_store,
    create_asset_from_file,
    make_client,
    wait_for_asset_ready,
    wait_for_item_ready,
)


def print_search_response(resp, label):
    print(f"\n[{label}] {len(resp.data)} result(s); "
          f"next_page_token={'set' if resp.next_page_token else 'none'}")
    for hit in resp.data:
        if hit.asset_type == "video":
            print(f"  video rank={hit.rank} item={hit.item_id} matches={len(hit.matches)}")
            for m in hit.matches[:3]:
                print(f"    {m.start_sec:.1f}-{m.end_sec:.1f}s modalities={m.modalities}")
        else:
            print(f"  image rank={hit.rank} item={hit.item_id}")
        if hit.metadata is not None:
            print(f"    metadata={hit.metadata}")


def demo_ingestion_config_variants(client):
    """Create a KS with each ingestion_config variant. ingestion_config is
    immutable after creation, so each variant needs its own store."""
    print("\n=== Ingestion config variants ===")

    # 1) No ingestion config.
    ks_plain = client.knowledge_stores.create(
        name=f"ks-plain-{uuid.uuid4()}",
        description="No enrichment config",
        metadata={"team": "qa", "purpose": "sdk-test"},
    )
    print(f"  plain: id={ks_plain.id} metadata={ks_plain.metadata}")

    # 2) Description-based enrichment.
    ks_desc = client.knowledge_stores.create(
        name=f"ks-desc-{uuid.uuid4()}",
        ingestion_config=IngestionConfig(
            enrichment_config=EnrichmentConfig_Description(
                description="Extract the main subject, setting, and mood of each shot."
            )
        ),
    )
    print(f"  description-enrichment: id={ks_desc.id}")

    # 3) JSON-schema enrichment. Note the platform's schema restrictions:
    #    root type must be object, every property needs a description, no
    #    nullable / composition / $ref keywords.
    ks_schema = client.knowledge_stores.create(
        name=f"ks-schema-{uuid.uuid4()}",
        ingestion_config=IngestionConfig(
            enrichment_config=EnrichmentConfig_JsonSchema(
                json_schema=EnrichmentConfigJsonSchemaJsonSchema(
                    type="object",
                    properties={
                        "subject": {
                            "type": "string",
                            "description": "The primary subject visible in the shot.",
                        },
                        "setting": {
                            "type": "string",
                            "description": "Where the shot takes place.",
                        },
                    },
                )
            )
        ),
    )
    print(f"  json-schema-enrichment: id={ks_schema.id}")

    for ks in (ks_plain, ks_desc, ks_schema):
        cleanup_knowledge_store(client, ks.id)


def demo_crud(client):
    print("\n=== Knowledge store CRUD ===")
    ks = client.knowledge_stores.create(name=f"ks-crud-{uuid.uuid4()}")
    print(f"  created: id={ks.id} name={ks.name}")

    retrieved = client.knowledge_stores.retrieve(knowledge_store_id=ks.id)
    print(f"  retrieved: id={retrieved.id} item_count={retrieved.item_count}")

    updated = client.knowledge_stores.update(
        knowledge_store_id=ks.id,
        name=f"ks-crud-updated-{uuid.uuid4()}",
        description="Updated description",
        metadata={"stage": "updated"},
    )
    print(f"  updated: name={updated.name} description={updated.description} metadata={updated.metadata}")

    # list() returns an auto-paginating SyncPager (consistent with
    # assets.list() / indexes.list()); iterate it directly.
    print("  listing knowledge stores (first few):")
    for i, item in enumerate(client.knowledge_stores.list(page_limit=5)):
        print(f"    id={item.id} name={item.name} item_count={item.item_count}")
        if i >= 4:
            break

    cleanup_knowledge_store(client, ks.id)


def demo_items(client, ks_id):
    print("\n=== Items ===")
    items = {}

    # Add a video and an image to the knowledge store. Upload each file as an
    # asset, wait for it to be ready, then create a knowledge store item from it.
    video_asset_id = create_asset_from_file(client, VIDEO_PATH)
    wait_for_asset_ready(client, video_asset_id)
    video_item = client.knowledge_store_items.create(
        knowledge_store_id=ks_id, asset_id=video_asset_id, asset_type="video"
    )
    items["video"] = video_item.id
    print(f"  created video item: id={video_item.id}")

    image_asset_id = create_asset_from_file(client, IMAGE_PATH)
    wait_for_asset_ready(client, image_asset_id)
    image_item = client.knowledge_store_items.create(
        knowledge_store_id=ks_id, asset_id=image_asset_id, asset_type="image"
    )
    items["image"] = image_item.id
    print(f"  created image item: id={image_item.id}")

    # Wait for both items to finish processing.
    for kind, item_id in items.items():
        print(f"  waiting for {kind} item {item_id} to be ready ...")
        wait_for_item_ready(client, ks_id, item_id)

    print("  list all items:")
    for it in client.knowledge_store_items.list(
        knowledge_store_id=ks_id, page_limit=50, sort_by="created_at", sort_option="desc"
    ):
        print(f"    id={it.id} type={it.asset_type} status={it.status}")

    print("  filter items by status=ready:")
    ready = list(client.knowledge_store_items.list(
        knowledge_store_id=ks_id, status=["ready"]
    ))
    print(f"    {len(ready)} ready item(s)")

    # Retrieve a single item.
    single = client.knowledge_store_items.retrieve(
        knowledge_store_id=ks_id, item_id=items["video"]
    )
    print(f"  retrieved item {single.id}: type={single.asset_type} "
          f"system_metadata={single.system_metadata is not None}")

    return items


def demo_item_collections(client, ks_id, items):
    print("\n=== Item collections ===")
    collection = client.knowledge_store_item_collections.create(
        knowledge_store_id=ks_id,
        name=f"collection-{uuid.uuid4()}",
        description="A subset of items",
        metadata={"group": "highlights"},
    )
    print(f"  created collection: id={collection.id} name={collection.name}")

    all_item_ids = list(items.values())
    client.knowledge_store_item_collections.add_items(
        knowledge_store_id=ks_id, collection_id=collection.id, item_ids=all_item_ids
    )
    print(f"  added {len(all_item_ids)} item(s) to collection")

    members = list(client.knowledge_store_item_collections.list_items(
        knowledge_store_id=ks_id, collection_id=collection.id
    ))
    print(f"  collection now has {len(members)} member item(s)")

    updated = client.knowledge_store_item_collections.update(
        knowledge_store_id=ks_id, collection_id=collection.id, description="Updated collection description"
    )
    print(f"  updated collection description={updated.description}")

    if all_item_ids:
        client.knowledge_store_item_collections.remove_items(
            knowledge_store_id=ks_id, collection_id=collection.id, item_ids=[all_item_ids[0]]
        )
        print(f"  removed 1 item from collection")

    print("  listing collections:")
    for c in client.knowledge_store_item_collections.list(knowledge_store_id=ks_id):
        print(f"    id={c.id} name={c.name}")

    client.knowledge_store_item_collections.delete(
        knowledge_store_id=ks_id, collection_id=collection.id
    )
    print(f"  deleted collection {collection.id}")


def demo_search(client, ks_id, items):
    print("\n=== Search ===")

    # `search_options` selects which video modalities to match on.
    visual_only = SearchKnowledgeStoreOptions(
        video=VideoSearchOptions(modalities=["visual"])
    )

    # 1) Basic search (individual matches).
    resp = client.knowledge_stores.search(
        knowledge_store_id=ks_id,
        query=KnowledgeStoreSearchQuery(text="a person or animal moving"),
        search_options=visual_only,
    )
    print_search_response(resp, "basic (visual)")

    # 2) group_by=item.
    resp = client.knowledge_stores.search(
        knowledge_store_id=ks_id,
        query=KnowledgeStoreSearchQuery(text="a person or animal moving"),
        search_options=visual_only,
        group_by="item",
    )
    print_search_response(resp, "group_by=item")

    # 3) Filter by asset_type = video, with multi-modality search options.
    resp = client.knowledge_stores.search(
        knowledge_store_id=ks_id,
        query=KnowledgeStoreSearchQuery(text="dialogue or narration"),
        filter=SearchKnowledgeStoreFilter(asset_type=AssetTypeFilter(eq="video")),
        search_options=SearchKnowledgeStoreOptions(
            video=VideoSearchOptions(
                modalities=["visual", "audio"],
            )
        ),
        include_metadata=True,
    )
    print_search_response(resp, "video-only + all modalities + metadata")

    # 4) Filter by specific item id.
    if "video" in items:
        resp = client.knowledge_stores.search(
            knowledge_store_id=ks_id,
            query=KnowledgeStoreSearchQuery(text="anything"),
            filter=SearchKnowledgeStoreFilter(item_id=ItemIdFilter(in_=[items["video"]])),
            search_options=visual_only,
        )
        print_search_response(resp, f"item_id in [{items['video']}]")

    # 5) Paginate with a small page_size, then fetch the next page with the token.
    resp = client.knowledge_stores.search(
        knowledge_store_id=ks_id,
        query=KnowledgeStoreSearchQuery(text="a person or animal moving"),
        search_options=visual_only,
        page_size=1,
    )
    print_search_response(resp, "page_size=1")
    if resp.next_page_token:
        page2 = client.knowledge_stores.search(
            knowledge_store_id=ks_id,
            query=KnowledgeStoreSearchQuery(text="a person or animal moving"),
            search_options=visual_only,
            page_size=1,
            page_token=resp.next_page_token,
        )
        print_search_response(page2, "page 2 (via next_page_token)")


def main():
    with make_client() as client:
        # Lightweight demos that don't need ready items.
        demo_ingestion_config_variants(client)
        demo_crud(client)

        # Full flow: create a store, add a video and an image item, then
        # exercise items, collections, and search against it.
        ks = client.knowledge_stores.create(name=f"ks-search-{uuid.uuid4()}")
        print(f"\nCreated knowledge store: id={ks.id} name={ks.name}")
        try:
            items = demo_items(client, ks.id)
            demo_item_collections(client, ks.id, items)
            demo_search(client, ks.id, items)
        finally:
            cleanup_knowledge_store(client, ks.id)


if __name__ == "__main__":
    main()
