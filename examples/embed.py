import os
from typing import List

import _context
from twelvelabs import TwelveLabs
from twelvelabs.models.embed import EmbeddingsTask, SegmentEmbedding


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:

    def print_segments(segments: List[SegmentEmbedding]):
        for segment in segments:
            print(
                f"  embedding_scope={segment.embedding_scope} start_offset_sec={segment.start_offset_sec} end_offset_sec={segment.end_offset_sec}"
            )
            print(f"  embeddings: {", ".join(str(segment.embeddings_float))}")

    embed_tasks = client.embed.task.list()
    for task in embed_tasks:
        print(
            f"Embedding task: id={task.id} status={task.status} created_at={task.created_at}"
        )
        if (
            task.video_embedding is not None
            and task.video_embedding.segments is not None
        ):
            print_segments(task.video_embedding.segments)

    def on_task_update(task: EmbeddingsTask):
        print(f"  Status={task.status}")

    model_name = "Marengo-retrieval-2.7"

    res = client.embed.create(
        model_name=model_name,
        text="man walking across the street",
        text_truncate="start",
    )
    print(f"Created text embedding: model_name={res.model_name}")
    if res.text_embedding is not None and res.text_embedding.segments is not None:
        print_segments(res.text_embedding.segments)

    res = client.embed.create(
        model_name=model_name,
        image_file=os.path.join(os.path.dirname(__file__), "assets/search_sample.png"),
    )
    print(f"Created image embedding: model_name={res.model_name}")
    if res.image_embedding is not None and res.image_embedding.segments is not None:
        print_segments(res.image_embedding.segments)

    res = client.embed.create(
        model_name=model_name,
        audio_file=os.path.join(os.path.dirname(__file__), "assets/audio_sample.mp3"),
    )
    print(f"Created audio embedding: model_name={res.model_name}")
    if res.audio_embedding is not None and res.audio_embedding.segments is not None:
        print_segments(res.audio_embedding.segments)

    task = client.embed.task.create(
        model_name=model_name,
        video_file=os.path.join(os.path.dirname(__file__), "assets/example.mp4"),
    )
    print(
        f"Created task: id={task.id} model_name={task.model_name} status={task.status}"
    )

    status = task.wait_for_done(callback=on_task_update)
    print(f"Embedding done: {status}")

    task = task.retrieve()
    if task.video_embedding is not None and task.video_embedding.segments is not None:
        print_segments(task.video_embedding.segments)
