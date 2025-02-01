import os
import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    video_id = "<YOUR_VIDEO_ID>"

    res = client.generate.summarize(video_id, "summary")
    print(f"Summary: {res.summary}")

    print("Chapters:")
    res = client.generate.summarize(video_id, "chapter")
    for chapter in res.chapters:
        print(
            f"  chapter_number={chapter.chapter_number} chapter_title={chapter.chapter_title} chapter_summary={chapter.chapter_summary} start={chapter.start} end={chapter.end}"
        )

    print("Highlights:")
    res = client.generate.summarize(video_id, "highlight")
    for highlight in res.highlights:
        print(
            f"  highlight={highlight.highlight} start={highlight.start} end={highlight.end}"
        )

    gist = client.generate.gist(video_id, ["title", "topic", "hashtag"])
    print(f"Gist: title={gist.title} topics={gist.topics} hashtags={gist.hashtags}")

    res = client.generate.text(video_id, "What happened?")
    print(f"Open-ended Text: {res.data}")

    text_stream = client.generate.text_stream(
        video_id=video_id, prompt="What happened?"
    )

    for text in text_stream:
        print(text)

    print(f"Aggregated text: {text_stream.aggregated_text}")
