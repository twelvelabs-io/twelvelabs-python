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

    # Basic analyze example
    res = client.analyze(
        video_id=video_id,
        prompt="What happened?",
    )
    print("Basic analyze result:")
    print(json.dumps(res.model_dump(), indent=2))

    # Advanced analyze with structured output and max_tokens
    res_structured = client.analyze(
        video_id=video_id,
        prompt="I want to generate a description for my video with the following format - Title of the video, followed by a summary in 2-3 sentences, highlighting the main topic, key events, and concluding remarks.",
        temperature=0.2,
        response_format=AnalyzeRequestResponseFormat(
            json_schema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "keywords": {"type": "array", "items": {"type": "string"}},
                },
            },
        ),
        max_tokens=2000,
    )
    print("\nStructured analyze result:")
    print(json.dumps(res_structured.model_dump(), indent=2))

    # Streaming analyze example
    res_stream = client.analyze_stream(
        video_id=video_id,
        prompt="What happened?",
    )
    print("\nStreaming analyze result:")
    for chunk in res_stream:
        if chunk.event_type == "text_generation":
            print(chunk.text, end="", flush=True)
        elif isinstance(chunk, StreamEndResponse):
            print(f"\nFinish reason: {chunk.finish_reason}")
            if chunk.metadata and chunk.metadata.usage:
                print(f"Usage: {chunk.metadata.usage}")
    print()  # Add newline after streaming

    # Streaming with structured output
    res_stream_structured = client.analyze_stream(
        video_id=video_id,
        prompt="Analyze this video and provide a structured breakdown of the main topics, key insights, and action items.",
        temperature=0.3,
        response_format=AnalyzeRequestResponseFormat(
            json_schema={
                "type": "object",
                "properties": {
                    "main_topics": {"type": "array", "items": {"type": "string"}},
                    "key_insights": {"type": "array", "items": {"type": "string"}},
                    "action_items": {"type": "array", "items": {"type": "string"}},
                },
            },
        ),
        max_tokens=1500,
    )
    print("\nStreaming structured analyze result:")
    for chunk in res_stream_structured:
        if chunk.event_type == "text_generation":
            print(chunk.text, end="", flush=True)
        elif isinstance(chunk, StreamEndResponse):
            print(f"\nFinish reason: {chunk.finish_reason}")
            if chunk.metadata and chunk.metadata.usage:
                print(f"Usage: {chunk.metadata.usage}")
    print()  # Add newline after streaming