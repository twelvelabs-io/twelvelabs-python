import os

from twelvelabs import TwelveLabs
from twelvelabs.models.task import Task
import uuid


def main():
    API_KEY = os.getenv("API_KEY")
    assert (
        API_KEY
    ), "Your API key should be stored in an environment variable named API_KEY."

    with TwelveLabs(API_KEY) as client:
        print(f"Client: base_url={client.base_url} api_key={client.api_key}")

        # Engine
        print("Available engines:")
        engines = client.engine.list()

        for engine in engines:
            print(
                f"id={engine.id} allowed_index_options={engine.allowed_index_options}"
            )

        # Index
        index = client.index.create(
            f"idx-{uuid.uuid4()}",
            [
                {
                    "name": "marengo2.5",
                    "options": ["visual", "conversation", "text_in_video", "logo"],
                }
            ],
        )
        client.index.update(index.id, f"idx-{uuid.uuid4()}")

        print("Indexes: ")
        indexes = client.index.list()
        for index in indexes:
            print(
                f"id={index.id} name={index.name} engines={index.engines} created_at={index.created_at}"
            )

        # Task
        print("Uploading an example video(example.mp4) and waiting for done")
        video_path = os.path.join(os.path.dirname(__file__), "resources/example.mp4")
        task = client.task.create(index.id, file=video_path, language="en")

        def on_task_update(task: Task):
            print(f"  Status={task.status}")

        task.wait_for_done(callback=on_task_update)

        if task.status != "ready":
            raise RuntimeError(f"Indexing failed with status {task.status}")
        print("Uploaded a video")


if __name__ == "__main__":
    main()
