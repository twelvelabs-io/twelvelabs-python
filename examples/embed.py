import os

import _context
from twelvelabs import TwelveLabs


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    engine_name = "Marengo-retrieval-2.6"
    embedding = client.embed.create(
        engine_name=engine_name,
        text="man walking across the street",
        text_truncate="start",
    )
    print(f"Created embedding: engine_name={embedding.engine_name}")

    video_path = os.path.join(os.path.dirname(__file__), "assets/example.mp4")
    task_id = client.embed.task.create(engine_name=engine_name, video_file=video_path)

    task = client.embed.task.retrieve(task_id)
    print(
        f"Created task: id={task.id} engine_name={task.engine_name} status={task.status}"
    )

    task_status = client.embed.task.status(task.id)
    print(f"Task status: {task_status.status}")
