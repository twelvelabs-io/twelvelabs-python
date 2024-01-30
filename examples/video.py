import os

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    index = client.index.retrieve("65a75560efa0814ef2edc77a")

    print(f"Videos in index id={index.id}")
    videos = client.index.video.list(index.id)
    for video in videos:
        print(
            f"  filename={video.metadata.filename} duration={video.metadata.duration}"
        )

    print(f"With pagigation: ")
    result = client.index.video.list_pagination(index.id)

    for task in result.data:
        print(
            f"  filename={video.metadata.filename} duration={video.metadata.duration}"
        )

    while True:
        try:
            next_page_data = next(result)
            print(f"Next page's data: {next_page_data}")
        except StopIteration:
            print("There is no next page in search result")
            break

    video = client.index.video.retrieve(index.id, videos[0].id)
    client.index.video.update(
        index.id, video.id, title="updated_test_video", metadata={"from_sdk": True}
    )
    print(f"Updated first video: id={video.id} metadata={video.metadata}")

    transcriptions = client.index.video.transcription(
        index.id, video.id, start=0, end=30
    )
    print(f"There are {str(len(transcriptions))} transcriptions")
    for transcription in transcriptions:
        print(
            f"  value={transcription.value} start={transcription.start} end={transcription.end}"
        )

    text_in_videos = client.index.video.text_in_video(
        index.id, video.id, start=0, end=30
    )
    print(f"There are {str(len(text_in_videos))} text_in_videos")
    for text_in_video in text_in_videos:
        print(
            f"  value={text_in_video.value} start={text_in_video.start} end={text_in_video.end}"
        )

    logos = client.index.video.logo(index.id, video.id)
    print(f"There are {str(len(logos))} logos")
    for logo in logos:
        print(f"  value={logo.value} start={logo.start} end={logo.end}")

    thumbnail = client.index.video.thumbnail(index.id, video.id)
    print(f"Thumbnail: {thumbnail}")
