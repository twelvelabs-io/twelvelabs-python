import os

import _context
from twelvelabs import TwelveLabs
from twelvelabs.models.task import Task


API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."

with TwelveLabs(API_KEY) as client:
    index = client.index.retrieve("<YOUR_INDEX_ID>")

    video_path = os.path.join(os.path.dirname(__file__), "assets/example.mp4")
    task = client.task.create(index.id, file=video_path, language="en")
    print(f"Created task: id={task.id} status={task.status}")

    print("Uploading an example video(example.mp4) and waiting for done")

    def on_task_update(task: Task):
        print(f"  Status={task.status}")

    task.wait_for_done(callback=on_task_update)

    if task.status != "ready":
        raise RuntimeError(f"Indexing failed with status {task.status}")
    print("Uploaded a video")

    print(f"Tasks in index {index.id}")
    tasks = client.task.list(index_id=index.id)
    for task in tasks:
        print(f"  id={task.id} status={task.status}")

    print(f"With pagigation: ")
    result = client.task.list_pagination()

    for task in result.data:
        print(f"  id={task.id} status={task.status}")

    while True:
        try:
            next_page_data = next(result)
            print(f"Next page's data: {next_page_data}")
        except StopIteration:
            print("There is no next page in search result")
            break

    status = client.task.status(index.id)
    print(
        f"Tasks by status: ready={status.ready} validating={status.validating} pending={status.pending} failed={status.failed} total_result={status.total_result}"
    )
