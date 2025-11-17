import os

from twelvelabs import TwelveLabs

API_KEY = os.getenv("API_KEY")
assert (
    API_KEY
), "Your API key should be stored in an environment variable named API_KEY."


with TwelveLabs(api_key=API_KEY) as client:
    index = client.indexes.retrieve(index_id="<YOUR_INDEX_ID>")

    video_path = os.path.join(os.path.dirname(__file__), "assets/example.mp4")

    with open(video_path, "rb") as video_file:
        task1 = client.tasks.create(index_id=index.id, video_file=video_file)
        print(f"Created task1: id={task1.id}")

    task2 = client.tasks.create(index_id=index.id, video_file=video_file)
    print(f"Created task2: id={task2.id}")
