import os

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    index = client.index.retrieve("<YOUR_INDEX_ID>")

    print(f"Videos in index id={index.id}")
    videos = client.index.video.list(index.id)
    if len(videos) == 0:
        print("No videos in the index, exiting")
        exit()

    for video in videos:
        print(
            f"  filename={video.system_metadata.filename} duration={video.system_metadata.duration}"
        )

    print(f"With pagigation: ")
    result = client.index.video.list_pagination(index.id)

    for task in result.data:
        print(
            f"  filename={video.system_metadata.filename} duration={video.system_metadata.duration}"
        )

    while True:
        try:
            next_page_data = next(result)
            print(f"Next page's data: {next_page_data}")
        except StopIteration:
            print("There is no next page in video list result")
            break

    client.index.video.update(
        index.id,
        videos[0].id,
        user_metadata={"from_sdk": True},
    )
    video = client.index.video.retrieve(index.id, videos[0].id)
    print(f"Updated first video: id={video.id} metadata={video.user_metadata}")

    # Get the first video and print its embeddings
    video = client.index.video.retrieve(index.id, videos[0].id, embedding_option=["visual-text", "audio"])

    if hasattr(video, 'embedding') and video.embedding and video.embedding.video_embedding:
        print("\nVideo Embeddings:")
        for i, segment in enumerate(video.embedding.video_embedding.segments):
            print(
                f"  embedding_scope={segment.embedding_scope} embedding_option={segment.embedding_option} start_offset_sec={segment.start_offset_sec} end_offset_sec={segment.end_offset_sec}"
            )
            first_few = segment.embeddings_float[:5]  # Show just first 5 values
            print(f"  embeddings: [{', '.join(str(x) for x in first_few)}...] (total: {len(segment.embeddings_float)} values)")