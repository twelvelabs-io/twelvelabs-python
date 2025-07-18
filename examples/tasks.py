import os

from twelvelabs import TwelveLabs
from twelvelabs.tasks import TasksRetrieveResponse

API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


with TwelveLabs(api_key=API_KEY) as client:
    index = client.indexes.retrieve(index_id="<YOUR_INDEX_ID>")

    video_path = os.path.join(os.path.dirname(__file__), "assets/example.mp4")
    with open(video_path, "rb") as video_file:
        task = client.tasks.create(index_id=index.id, video_file=video_file)

    print(f"Created task: id={task.id}")

    print("Uploading an example video(example.mp4) and waiting for done")

    def on_task_update(task: TasksRetrieveResponse):
        print(f"  Status={task.status}")

    task = client.tasks.wait_for_done(task_id=task.id, callback=on_task_update)

    if task.status != "ready":
        raise RuntimeError(f"Indexing failed with status {task.status}")
    print("Uploaded a video")

    print(f"Tasks in index {index.id}")
    tasks_pager = client.tasks.list(index_id=index.id)
    if len(tasks_pager.items) == 0:
        print("No tasks in the index, exiting")
        exit()
    for task in tasks_pager:
        print(f"  id={task.id} status={task.status} created_at={task.created_at}")
