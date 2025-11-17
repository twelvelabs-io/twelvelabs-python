import os
from typing import List
import base64

from twelvelabs import TwelveLabs
from twelvelabs.types import (
    TextInputRequest,
    ImageInputRequest,
    AudioInputRequest,
    VideoInputRequest,
    EmbeddingData,
    MediaSource,
    EmbeddingTaskResponse,
)


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


with TwelveLabs(api_key=API_KEY) as client:

    model_name = "marengo3.0"

    def print_embeddings(embeddings: List[EmbeddingData]):
        for embedding in embeddings:
            print(
                f"Embedding: [{', '.join(str(x) for x in embedding.embedding[:5])}...] (total: {len(embedding.embedding)} values)"
            )
            if embedding.embedding_option is not None:
                print(f"Embedding option: {embedding.embedding_option}")
            if embedding.embedding_scope is not None:
                print(f"Embedding scope: {embedding.embedding_scope}")
            if embedding.start_sec is not None:
                print(f"Start sec: {embedding.start_sec}")
            if embedding.end_sec is not None:
                print(f"End sec: {embedding.end_sec}")

    embed_tasks_pager = client.embed.v_2.tasks.list()
    for task in embed_tasks_pager:
        print(
            f"Embed task: id={task.id} status={task.status} created_at={task.created_at}"
        )

    # Sync embedding examples

    # text embedding
    res = client.embed.v_2.create(
        input_type="text",
        model_name=model_name,
        text=TextInputRequest(
            input_text="man walking across the street",
        ),
    )
    print(f"Created text embedding")
    if res.data is not None and len(res.data) > 0:
        print_embeddings(res.data)

    # image embedding (using url)
    res = client.embed.v_2.create(
        input_type="image",
        model_name=model_name,
        image=ImageInputRequest(
            media_source=MediaSource(url="https://www.gstatic.com/webp/gallery/1.jpg")
        ),
    )
    print(f"Created image embedding")
    if res.data is not None and len(res.data) > 0:
        print_embeddings(res.data)

    # image embedding (using base64)
    image_path = os.path.join(os.path.dirname(__file__), "assets/search_sample.png")
    with open(image_path, "rb") as image_file:
        base_64_string = base64.b64encode(image_file.read()).decode("utf-8")
        res = client.embed.v_2.create(
            input_type="image",
            model_name=model_name,
            image=ImageInputRequest(
                media_source=MediaSource(base_64_string=base_64_string)
            ),
        )
        print(f"Created image embedding")
        if res.data is not None and len(res.data) > 0:
            print_embeddings(res.data)

    # audio embedding (sync, short audio using base64)
    audio_path = os.path.join(os.path.dirname(__file__), "assets/audio_sample.mp3")
    with open(audio_path, "rb") as audio_file:
        base_64_string = base64.b64encode(audio_file.read()).decode("utf-8")
        res = client.embed.v_2.create(
            input_type="audio",
            model_name=model_name,
            audio=AudioInputRequest(
                media_source=MediaSource(base_64_string=base_64_string)
            ),
        )
        print(f"Created audio embedding")
        if res.data is not None and len(res.data) > 0:
            print_embeddings(res.data)

    # video embedding (sync, short video using base64)
    video_path = os.path.join(os.path.dirname(__file__), "assets/example.mp4")
    with open(video_path, "rb") as video_file:
        base_64_string = base64.b64encode(video_file.read()).decode("utf-8")
    res = client.embed.v_2.create(
        input_type="video",
        model_name=model_name,
        video=VideoInputRequest(
            media_source=MediaSource(base_64_string=base_64_string)
        ),
    )
    print(f"Created video embedding")
    if res.data is not None and len(res.data) > 0:
        print_embeddings(res.data)

    # Async embedding examples

    def wait_for_done(task_id: str) -> EmbeddingTaskResponse:
        import time
        task = client.embed.v_2.tasks.retrieve(task_id)
        done_statuses = ["ready", "failed"]
        while task.status not in done_statuses:
            time.sleep(5)
            task = client.embed.v_2.tasks.retrieve(task_id)
            print(f"Task status: {task.status}")
        return task

    # video embedding (async using url)
    task = client.embed.v_2.tasks.create(
        input_type="video",
        model_name=model_name,
        video=VideoInputRequest(
            media_source=MediaSource(url="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")
        ),
    )
    print(f"Created video embedding task: id={task.id}")
    task = wait_for_done(task.id)
    print(f"Video embedding done: {task.status}")
    if task.data is not None and len(task.data) > 0:
        print_embeddings(task.data)

    # audio embedding (async using url)
    task = client.embed.v_2.tasks.create(
        input_type="audio",
        model_name=model_name,
        audio=AudioInputRequest(
            media_source=MediaSource(url="https://github.com/twelvelabs-io/twelvelabs-python/raw/refs/heads/main/examples/assets/audio_sample.mp3")
        ),
    )
    print(f"Created audio embedding task: id={task.id}")
    task = wait_for_done(task.id)
    print(f"Audio embedding done: {task.status}")
    if task.data is not None and len(task.data) > 0:
        print_embeddings(task.data)