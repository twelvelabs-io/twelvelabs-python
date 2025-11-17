import os

from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


with TwelveLabs(api_key=API_KEY) as client:
    index = client.indexes.retrieve(index_id="<YOUR_INDEX_ID>")

    print("\nSearch (group by video):")
    search_pager = client.search.query(
        index_id=index.id,
        search_options=["visual", "audio", "transcription"],
        query_text="A man talking",
        group_by="video",
    )
    for group in search_pager:
        if group.clips is None:
            continue
        print(f"  Video ID: {group.id}")
        for clip in group.clips:
            print(f"  rank={clip.rank} start={clip.start} end={clip.end}")

    print("\nSearch (no grouping):")
    search_pager = client.search.query(
        index_id=index.id,
        search_options=["visual", "audio", "transcription"],
        query_text="A man talking",
    )
    for clip in search_pager:
        print(f"  rank={clip.rank} start={clip.start} end={clip.end}")

    print("\nSearch (semantic transcription only):")
    search_pager = client.search.query(
        index_id=index.id,
        search_options=["transcription"],
        transcription_options=["semantic"],  # also supports "lexical"
        query_text="couple of chemicals",
    )
    for clip in search_pager:
        print(
            f"  rank={clip.rank} start={clip.start} end={clip.end} transcription={clip.transcription}"
        )

    print("Search by image:")
    image_path = os.path.join(os.path.dirname(__file__), "assets/search_sample.png")
    with open(image_path, "rb") as image_file:
        search_pager = client.search.query(
            index_id=index.id,
            search_options=["visual"],
            query_media_type="image",
            query_media_file=image_file,
        )
    for clip in search_pager:
        print(f"  rank={clip.rank} start={clip.start} end={clip.end}")

    print("Composed text and image search:")
    with open(image_path, "rb") as image_file:
        search_pager = client.search.query(
            index_id=index.id,
            search_options=["visual", "audio"],
            query_text="A man talking",
            query_media_type="image",
            query_media_file=image_file,
        )
        for clip in search_pager:
            print(f"  rank={clip.rank} start={clip.start} end={clip.end}")
