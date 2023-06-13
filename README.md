# Twelve Labs Python SDK

This SDK provides a convenient way to interact with the Twelve Labs Video Understanding Platform from an application written in the Python language. The SDK equips you with a set of intuitive classes and methods that streamline the process of interacting with the platform, reducing the boilerplate code you have to write.

## Prerequisites

Before using the SDK, ensure that you have the following prerequisites:

-  [Python](https://www.python.org) must be installed on your machine.
-  An active API key. If you don't have one, please [sign up](https://api.twelvelabs.io/) for a free account. Then, to retrieve your API key, go to the [Dashboard](https://api.twelvelabs.io/dashboard) page, and select the **Copy** button under the **API** Key section.

## Installation

**Question**: Do we want to encourage them to use [virtualenv](https://virtualenv.pypa.io/en/latest/) and  [asyncio](https://docs.python.org/3/library/asyncio.html)?

To install the SDK, follow the steps below:

TODO

## Initialization

1. Import the SDK and the `asyncio`  library into your project:

	```Python
	import asyncio
	from twelvelabs import APIClient
	``` 

2. Instantiate the SDK client with your API key. This example code assumes that your API key is stored in an environment variable named `API_KEY`:

	```Python
	async def main():
		API_KEY = os.getenv("API_KEY")
		assert API_KEY, "Your API key should be stored in an environment variable named API_KEY."
		async with APIClient(API_KEY) as client:
			# Perform desired actions using the `client` object

	if __name__ == "__main__":
			loop = asyncio.get_event_loop()
			loop.run_until_complete(main())
	```

## Usage

This section provides a guide on how to use the SDK to create an index, upload a video, and perform a search request.
### Create an Index

To create an index, use the example code below, replacing `example_index` with the desired name for your index:

```Python
print("Creating a new index named 'example_index' with default options")
index = await client.create_index("example_index")
print(f"Created an index: {index.name}({index.id})")
```
 

### Upload a video

To upload a video to your index, use the example code below, replacing `resources/example.mp4` with the actual file path of your video and ensuring that the video file meets the following requirements:
- **Video resolution**: must be greater than or equal to 360p and less than or equal to 1080p (FHD).
- **File size**: must not exceed 2 GB.
- **Duration**: must be between 10 seconds and 2 hours (7,200s).

```Python
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
```

### Perform a Search Request

To perform a search request, use the example code below:

```Python
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
```
