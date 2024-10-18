import os

import _context
from twelvelabs import TwelveLabs
from twelvelabs.models.embed import EmbeddingsTask


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    embed_tasks = client.embed.task.list()
    for task in embed_tasks:
        print(
            f"Embedding task: id={task.id} status={task.status} created_at={task.created_at}"
        )
        if task.metadata is not None:
            print(f"  metadata: {task.metadata}")

    def on_task_update(task: EmbeddingsTask):
        print(f"  Status={task.status}")

    engine_name = "Marengo-retrieval-2.6"

    res = client.embed.create(
        engine_name=engine_name,
        text="man walking across the street",
        text_truncate="start",
    )
    print(f"Created text embedding: engine_name={res.engine_name}")
    if res.text_embedding is not None:
        print(f"  embeddings: {", ".join(str(res.text_embedding.values))}")

    res = client.embed.create(
        engine_name=engine_name,
        image_file=os.path.join(os.path.dirname(__file__), "assets/search_sample.png"),
    )
    print(f"Created image embedding: engine_name={res.engine_name}")
    if res.image_embedding is not None:
        print(f"  embeddings: {", ".join(str(res.image_embedding.values))}")

    res = client.embed.create(
        engine_name=engine_name,
        audio_file=os.path.join(os.path.dirname(__file__), "assets/audio_sample.png"),
    )
    print(f"Created audio embedding: engine_name={res.engine_name}")
    if res.audio_embedding is not None and res.audio_embedding.segments is not None:
        for segment in res.audio_embedding.segments:
            print(
                f"  embedding_scope={segment.embedding_scope} start_offset_sec={segment.start_offset_sec} end_offset_sec={segment.end_offset_sec}"
            )
            print(f"  embeddings: {", ".join(str(segment.values))}")

    task = client.embed.task.create(
        engine_name=engine_name,
        video_file=os.path.join(os.path.dirname(__file__), "assets/example.mp4"),
    )
    print(
        f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}"
    )

    status = task.wait_for_done(callback=on_task_update)
    print(f"Embedding done: {status}")

    task = task.retrieve()
    if task.video_embeddings is not None:
        for v in task.video_embeddings:
            print(
                f"embedding_scope={v.embedding_scope} start_offset_sec={v.start_offset_sec} end_offset_sec={v.end_offset_sec}"
            )
            print(f"embeddings: {", ".join(str(v.values))}")
