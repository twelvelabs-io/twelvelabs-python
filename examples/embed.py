import os

import _context
from twelvelabs import TwelveLabs
from twelvelabs.models.embed import EmbeddingsTask


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:

    def print_video_embeddings(id: str):
        task = client.embed.task.retrieve(id)
        if task.video_embeddings is not None:
            for v in task.video_embeddings:
                print(
                    f"embedding_scope={v.embedding_scope} start_offset_sec={v.start_offset_sec} end_offset_sec={v.end_offset_sec}"
                )
                print(f"embeddings: {", ".join(str(v.embedding.values))}")

    def on_task_update(task: EmbeddingsTask):
        print(f"  Status={task.status}")

    engine_name = "Marengo-retrieval-2.6"

    embedding_text = client.embed.create(
        engine_name=engine_name,
        text="man walking across the street",
        text_truncate="start",
    )
    print(f"Created text embedding: engine_name={embedding_text.engine_name}")

    video_path = os.path.join(os.path.dirname(__file__), "assets/example.mp4")
    task = client.embed.task.create(engine_name=engine_name, video_file=video_path)
    print(
        f"Created task of text embedding: id={task.id} engine_name={task.engine_name} status={task.status}"
    )

    status = task.wait_for_done(callback=on_task_update)
    print(f"Embedding done: {status}")
    print_video_embeddings(task.id)

    embedding_image = client.embed.create(
        engine_name=engine_name,
        image_file=os.path.join(os.path.dirname(__file__), "assets/search_sample.png"),
    )
    print(f"Created image embedding: engine_name={embedding_image.engine_name}")

    video_path = os.path.join(os.path.dirname(__file__), "assets/example.mp4")
    task = client.embed.task.create(engine_name=engine_name, video_file=video_path)
    print(
        f"Created task of image embedding: id={task.id} engine_name={task.engine_name} status={task.status}"
    )

    status = task.wait_for_done(callback=on_task_update)
    print(f"Embedding done: {status}")
    print_video_embeddings(task.id)
