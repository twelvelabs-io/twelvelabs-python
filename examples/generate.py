import os

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    index = client.index.retrieve("65a75560efa0814ef2edc77a")
    videos = client.index.video.list(index.id)
    if len(videos) == 0:
        print(f"No videos in index {index.id}, exit")
        exit()
    video = videos[0]

    gist = client.generate.gist(video.id, ["title"])
    print(f"Gist: title={gist.title} topics={gist.topics} hashtags={gist.hashtags}")

    res = client.generate.summarize(video.id, "summary")
    print(f"Summary: {res.summary}")

    print("Chapters:")
    res = client.generate.summarize(video.id, "chapter")
    for chapter in res.chapters:
        print(
            f"  chapter_number={chapter.chapter_number} chapter_title={chapter.chapter_title} chapter_summary={chapter.chapter_summary} start={chapter.start} end={chapter.end}"
        )

    print("Highlights:")
    res = client.generate.summarize(video.id, "highlight")
    for highlight in res.highlights:
        print(
            f"  highlight={highlight.highlight} start={highlight.start} end={highlight.end}"
        )

    res = client.generate.text(video.id, "What happened?")
    print(f"Open-ended Text: {res.data}")
