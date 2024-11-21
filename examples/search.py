import os

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    index = client.index.retrieve("<YOUR_INDEX_ID>")
    search_options = ["visual", "audio"]

    print("Search (group by video):")
    result = client.search.query(
        index.id,
        search_options,
        query_text="Train",
        group_by="video",
    )
    for group in result.data:
        print(f"  group.id={group.id}")
        for clip in group.clips:
            print(
                f"  score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"
            )

    print("Search:")
    result = client.search.query(
        index.id,
        search_options,
        query_text="A man talking",
    )
    for clip in result.data:
        print(
            f"  score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"
        )

    while True:
        try:
            next_page_data = next(result)
            print(f"Next page's data")
            for clip in next_page_data:
                print(
                    f"  score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"
                )
        except StopIteration:
            print("There is no next page in search result")
            break

    print("Search by image:")
    image_path = os.path.join(os.path.dirname(__file__), "assets/search_sample.png")
    result = client.search.query(
        index.id,
        search_options,
        query_media_type="image",
        query_media_file=image_path,
    )
    for clip in result.data:
        print(
            f"  score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"
        )

    while True:
        try:
            next_page_data = next(result)
            print(f"Next page's data")
            for clip in next_page_data:
                print(
                    f"  score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"
                )
        except StopIteration:
            print("There is no next page in search result")
            break
