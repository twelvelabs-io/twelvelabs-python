import os

from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


with TwelveLabs(api_key=API_KEY) as client:
    index = client.indexes.retrieve("<YOUR_INDEX_ID>")

    print(f"Videos in index id={index.id}")
    videos_pager = client.indexes.videos.list(index.id)
    if len(videos_pager.items) == 0:
        print("No videos in the index, exiting")
        exit()
    for video in videos_pager:
        print(
            f"  id={video.id} filename={video.system_metadata.filename} duration={video.system_metadata.duration}"
        )

    video = videos_pager.items[0]
    client.indexes.videos.update(index.id, video.id, user_metadata={"from_sdk": True})
    video = client.indexes.videos.retrieve(index.id, video.id)
    print(f"user_metadata={video.user_metadata}")

    video = client.indexes.videos.retrieve(
        index.id, video.id, embedding_option=["visual", "audio"]
    )
    if video.embedding and video.embedding.video_embedding:
        print("\nVideo Embeddings:")
        for i, segment in enumerate(video.embedding.video_embedding.segments):
            print(
                f"  embedding_scope={segment.embedding_scope} embedding_option={segment.embedding_option} start_offset_sec={segment.start_offset_sec} end_offset_sec={segment.end_offset_sec}"
            )
            # TODO currently embeddings_float does not exist
            # first_few = segment.embeddings_float[:5]  # Show just first 5 values
            # print(f"  embeddings: [{', '.join(str(x) for x in first_few)}...] (total: {len(segment.embeddings_float)} values)")
