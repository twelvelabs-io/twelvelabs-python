import asyncio
import os

from twelvelabs import APIClient
from twelvelabs.api.task import Task


async def main():
    API_KEY = "tlk_29V2AQA2J7PG0Q2H7V71724W2KEP"

    async with APIClient(API_KEY) as client:
        print("Available engines:")
        engines = await client.get_engines()
        for engine in engines:
            print(
                f"id={engine.id} allowed_index_options={engine.allowed_index_options}"
            )

        print("Creating a new index named 'example_index' with default options")
        index = await client.create_index("example_index")

        print(f"Created an index: {index.name}({index.id})")

        print("Uploading an example video(example.mp4)")
        video_path = os.path.join(os.path.dirname(__file__), "resources/example.mp4")
        task = await index.upload_video(file=video_path, language="en")

        def on_task_update(task: Task):
            print(f"  Status={task.status}")

        print("Waiting the indexing task to be done")
        await task.wait(
            on_task_update, sleep_interval=10
        )  # Check status every 10 seconds

        if task.status != "ready":
            raise RuntimeError(f"Indexing failed with status {task.status}")

        # Get the latest video which we just uploaded
        video = (await index.get_videos(sort_by="created_at", sort_option="desc"))[0]
        print(f"Successfully indexed a video: {video.id}")

        def print_search_result(res):
            for clip in res:
                print(
                    f'  score={clip["score"]} start={clip["start"]} end={clip["end"]} confidence={clip["confidence"]}'
                )

        print("Searching for a query 'A man talking")
        r = await index.search("A man talking", options=["visual", "conversation"])
        print_search_result(r.data)
        async for res in r:
            print_search_result(res)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
