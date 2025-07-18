import os

from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


with TwelveLabs(api_key=API_KEY) as client:
    video_id = "<YOUR_VIDEO_ID>"

    res = client.summarize(
        video_id=video_id,
        type="summary",
    )
    if res.summarize_type == "summary":
        print(f"Summary: {res.summary}")

    res = client.summarize(
        video_id=video_id,
        type="chapter",
    )
    if res.summarize_type == "chapter":
        for chapter in res.chapters:
            print(
                f"  chapter_number={chapter.chapter_number} chapter_title={chapter.chapter_title} chapter_summary={chapter.chapter_summary} start={chapter.start} end={chapter.end}"
            )

    res = client.summarize(
        video_id=video_id,
        type="highlight",
    )
    if res.summarize_type == "highlight":
        for highlight in res.highlights:
            print(
                f"  highlight={highlight.highlight} start={highlight.start} end={highlight.end}"
            )

    gist = client.gist(
        video_id=video_id,
        types=["title", "topic", "hashtag"],
    )
    print(f"Gist: title={gist.title} topics={gist.topics} hashtags={gist.hashtags}")

    res = client.analyze(
        video_id=video_id,
        prompt="What happened?",
    )
    print(res.data)

    res_stream = client.analyze_stream(
        video_id=video_id,
        prompt="What happened?",
    )
    for chunk in res_stream:
        if chunk.event_type == "text_generation":
            print(chunk.text)
