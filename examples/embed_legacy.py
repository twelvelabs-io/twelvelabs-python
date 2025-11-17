import os
from typing import List

from twelvelabs import TwelveLabs
from twelvelabs.types import BaseSegment
from twelvelabs.embed import TasksStatusResponse

API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


with TwelveLabs(api_key=API_KEY) as client:

    def print_segments(segments: List[BaseSegment]):
        for segment in segments:
            first_few = (
                segment.float_[:5] if segment.float_ else []
            )  # Show just first 5 values
            print(
                f"  embeddings: [{', '.join(str(x) for x in first_few)}...] (total: {len(segment.float_) if segment.float_ else 0} values)"
            )

    embed_tasks_pager = client.embed.tasks.list()
    for task in embed_tasks_pager:
        print(
            f"Embedding task: id={task.id} status={task.status} created_at={task.created_at}"
        )

    model_name = "marengo3.0"

    res = client.embed.create(
        model_name=model_name,
        text="man walking across the street",
        text_truncate="start",
    )
    print(f"Created text embedding")
    if res.text_embedding is not None and res.text_embedding.segments is not None:
        print_segments(res.text_embedding.segments)

    image_path = os.path.join(os.path.dirname(__file__), "assets/search_sample.png")
    with open(image_path, "rb") as image_file:
        res = client.embed.create(
            model_name=model_name,
            image_file=image_file,
        )
    print(f"Created image embedding")
    if res.image_embedding is not None and res.image_embedding.segments is not None:
        print_segments(res.image_embedding.segments)

    audio_path = os.path.join(os.path.dirname(__file__), "assets/audio_sample.mp3")
    with open(audio_path, "rb") as audio_file:
        res = client.embed.create(
            model_name=model_name,
            audio_file=audio_file,
        )
    print(f"Created audio embedding")
    if res.audio_embedding is not None and res.audio_embedding.segments is not None:
        print_segments(res.audio_embedding.segments)

    video_path = os.path.join(os.path.dirname(__file__), "assets/example.mp4")
    with open(video_path, "rb") as video_file:
        task = client.embed.tasks.create(
            model_name=model_name,
            video_file=video_file,
        )
    print(f"Created video embedding task: id={task.id}")

    def on_task_update(task: TasksStatusResponse):
        print(f"  Status={task.status}")

    status = client.embed.tasks.wait_for_done(task.id, callback=on_task_update)
    print(f"Embedding done: {status.status}")

    # Retrieve the task with the specified embedding option: "visual-text".
    # If you don't specify the embedding option, it will return all available multi-vector embeddings.
    task = client.embed.tasks.retrieve(
        task_id=task.id, embedding_option=["visual-text"]
    )
    if task.video_embedding is not None and task.video_embedding.segments is not None:
        print_segments(task.video_embedding.segments)
