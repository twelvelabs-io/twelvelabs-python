import os

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    embedding = client.embed.create(
        engine_name="test_engine",
        text="man walking across the street",
        text_truncate="start",
    )

    video_path = os.path.join(os.path.dirname(__file__), "assets/example.mp4")
    task_id = client.embed.create_task(
        engine_name=embedding.engine_name, video_file=video_path
    )

    task = client.embed.retrieve_task(task_id)
    print(
        f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}"
    )
    for v in task.video_embeddings:
        print(
            f"  embedding_scope={v.embedding_scope} start_offset_sec={v.start_offset_sec} end_offset_sec={v.end_offset_sec} embedding={v.embedding.float}"
        )

    task_status = client.embed.task_status(task.id)
    print(f"Task status: {task_status.status}")
