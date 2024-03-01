import os

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    index = client.index.retrieve("65a75560efa0814ef2edc77a")

    print("Search (group by video):")
    result = client.search.query(
        index.id, "A man talking", ["visual", "conversation"], group_by="video"
    )
    for group in result.data:
        print(f"  {group.id} {group.clips}")

    print("Search:")
    result = client.search.query(index.id, "A man talking", ["visual", "conversation"])
    for clip in result.data:
        print(
            f"  score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"
        )

    while True:
        try:
            next_page_data = next(result)
            print(f"Next page's data: {next_page_data}")
        except StopIteration:
            print("There is no next page in search result")
            break
