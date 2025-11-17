import os

from twelvelabs import TwelveLabs

API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


sample_image_urls = [
    "https://www.gstatic.com/webp/gallery/1.jpg",
    "https://www.gstatic.com/webp/gallery/2.jpg",
    "https://www.gstatic.com/webp/gallery/3.jpg"
]


with TwelveLabs(api_key=API_KEY) as client:
    # Create assets
    asset_ids = []
    for i, url in enumerate(sample_image_urls, 1):
        asset = client.assets.create(
            method="url",
            url=url,
        )
        asset_ids.append(asset.id)
        print(f"Created asset {i}/5: id={asset.id}")

    print(f"Asset IDs: {asset_ids}")

    # Create entity collection
    entity_collection = client.entity_collections.create(
        name="Sample Entity Collection",
    )
    print(f"Created entity collection: id={entity_collection.id}")

    # Create entity
    entity = client.entity_collections.entities.create(
        entity_collection_id=entity_collection.id,
        name="Sample Entity",
        asset_ids=asset_ids,
    )
    print(f"Created entity: id={entity.id}")

    # Perform Entity Search
    index_id = "<YOUR_INDEX_ID>"

    search_pager = client.search.query(
        index_id=index_id,
        search_options=["visual", "audio"],
        # to perform entity search, the entity id should be wrapped with <@ and >
        query_text=f"<@{entity.id}> is walking",
    )
    for clip in search_pager:
        print(
            f"  video_id={clip.video_id} start={clip.start} end={clip.end} rank={clip.rank}"
        )
