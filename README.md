# TwelveLabs Python SDK

This SDK provides a convenient way to interact with the Twelve Labs Video Understanding Platform from an application written in the Python language. The SDK equips you with a set of intuitive classes and methods that streamline the process of interacting with the platform, minimizing the need for boilerplate code.


## Prerequisites

Ensure that the following prerequisites are met before using the SDK:

-  [Python](https://www.python.org) must be installed on your machine.
-  The API key of your account. If you don't have an account, please [sign up](https://api.twelvelabs.io/) for a free account. Then, to retrieve your API key, go to the [Dashboard](https://api.twelvelabs.io/dashboard) page, and select the **Copy** icon to the right of the key to copy it to your clipboard.

## Install the SDK

To install the SDK enter the following command in a terminal window:

```sh
pip install twelvelabs
```

## Initialize the SDK

1. Import the SDK into your application:

```py
from twelvelabs import TwelveLabs
```

2.  Instantiate the SDK client with your API key. This example code assumes that your API key is stored in an environment variable named `TL_API_KEY`:

```py
client = TwelveLabs(os.getenv('TL_API_KEY'))
```

## Use the SDK

To get started with the SDK, follow these basic steps:

1. Create an index.
2. Upload videos.
3. Perform downstream tasks, such as search.

## Create an index

To create an index, use the example code below, replacing `<YOUR_INDEX_NAME` with the desired name for your index:

```py
from twelvelabs import APIStatusError
from twelvelabs import APIStatusError
index_obj = None
try:
    index_obj = client.index.create(
        name = "<YOUR_INDEX_NAME>",
        engines =[
            {
                "name": "marengo2.5",
                "options": ["visual", "conversation", "text_in_video"],
            },
            {
                "name": "pegasus1",
                "options": ["visual", "conversation"],
            },
        ],
    )
    print(index_obj)
except APIStatusError as e:
    print('API Status Error, 4xx or 5xx')
    print(e)
except Exception as e:
    print(e)
```

The output should look similar to the following:

```
Index(id='65b1b926560f741da96836d7', created_at='2024-01-25T01:28:06.061Z', updated_at='2024-01-25T01:28:06.061Z', name='test-index-to-researchers1', engines=[Engine(name='marengo2.5', options=['visual', 'conversation', 'text_in_video'], addons=None), Engine(name='pegasus1', options=['visual', 'conversation'], addons=None)], video_count=0, total_duration=0.0, expires_at='2024-04-24T01:28:06.061Z')
```

Note that the API returns, among other information, a field named `id` representing the unique identifier of your new index.

See the [Create an index](https://docs.twelvelabs.io/v1.2/reference/create-index) page for more details about creating indexes.


## Upload videos

To upload a video to your index, use the example code below, replacing `./assets/*.mp4` with the actual file path of your videos and ensuring that the each video file meets the following requirements:
- **Video resolution**: Must be greater or equal than 360p and less or equal than 4K. For consistent search results, Twelve Labs recommends you upload 360p videos.
- **Duration**: For Marengo, it must be between 4 seconds and 2 hours (7,200s). For Pegasus, it must be between 5 seconds and 30 minutes (1800s).
- **File size**: Must not exceed 2 GB. If you require different options, send us an email at support@twelvelabs.io.
- **Audio track**: If the `conversation` [engine option](https://docs.twelvelabs.io/v1.2/docs/engine-options) is selected, the video you're uploading must contain an audio track.


```py
from glob import glob
video_paths = glob("./assets/*.mp4")
for video_path in video_paths[:1]:
    print(video_path)
    task = client.task.create(index_obj.id, file=video_path, language="en")

    print(f"Uploading {video_path} and waiting for the indexing process to be completed.")
    print(f"Created task: id={task.id}, status={task.status}")

    def on_task_update(task):
        print(f"  Status={task.status}")

    task.wait_for_done(callback=on_task_update)

    if task.status != "ready":
        raise RuntimeError(f"Indexing failed with status {task.status}")
    print(f"Uploaded {video_path}")
```
See the [Create a video indexing task](https://docs.twelvelabs.io/reference/create-video-indexing-task) page for more details.

## Perform downstream tasks

### Search

To perform a search request, use the example code below, replacing the following:

- **"<YOUR_QUERY>"**: A string representing your search query. Note that the API supports full natural language-based search. The following examples are valid queries: "birds flying near a castle", and "sun shining on water", and "an officer holding a child's hand."
- **"<YOUR_SEARCH_OPTIONS>"**: An array string that specifies the sources of information the platform uses when performing a search. For example, to search based on visual and conversation cues, use `["visual", "conversation"]`. For details, see the [Search options](https://docs.twelvelabs.io/docs/search-options) page.

```py
result = client.search.query(index_obj.id, "<YOUR_QUERY>", "<YOUR_SEARCH_OPTIONS>")
for clip in result.data:
    print(
        f"  score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"
    )

while True:
    try:
        next_page_data = next(result)
        print(f"Next page's data: {next_page_data}")
    except StopIteration:
        print("You've reached the end of the data set.")
        break
```

See the [Make a search request](/reference/make-search-request) page for more details.

---

## For Internal Test

Since it's before uploading to PyPI, you will install the package in editable mode after cloning the git repository.

```sh
git clone https://github.com/twelvelabs-io/twelvelabs-python
cd twelvelabs-python
pip install -e .
```

Afterward, you can import and use the package from your repository.

```python
from twelvelabs import TwelveLabs
client = TwelveLabs("<YOUR_API_KEY>")

engines = client.engine.list()
```

If you want to use development environment, set `TWELVELABS_BASE_URL` to enviroment variables. It'll automatically applied to your client.

## Installation

> Not supported yet

```sh
pip install twelvelabs
```

## Usage

All APIs of this library can be found in the `API.md` file. Additionally, the `examples` folder contains sample files categorized by their functionality.

```python
import os

from twelvelabs import TwelveLabs

client = TwelveLabs(os.getenv("TWELVELABS_API_KEY"))
client.index.create(
        f"my_index",
        [
            {
                "name": "pegasus1",
                "options": ["visual", "conversation"],
            },
        ],
        addons=["thumbnail"],
    )
```

When initializing the client, you must provide the API Key issued from the TwelveLabs Dashboard. Be cautious not to store the API Key in source control when using it. Currently, only synchronous usage is supported, and API communications are handled through httpx. (Support for an Async Client is planned for the future.)

## Error Handling

All errors are included in the twelvelabs package. If there is an issue connecting to the API, a twelvelabs.APIConnectionError will be raised. Errors like 4xx and 5xx status codes can be imported and handled according to the specific status code that occurs.

```python
import os

from twelvelabs import TwelveLabs

client = TwelveLabs(os.getenv("TWELVELABS_API_KEY"))
try:
    engines = client.engines.list()
    print(engines)
except twelvelabs.APIConnectionError as e:
    print("Cannot connect to API server")
except twelvelabs.BadRequestError as e:
    print("Bad request, please refer to api docs")
except twelvelabs.APIStatusError as e:
    print(f"Status code {e.status_code} received")
    print(e.response)
```

## TODO

- cli
- validate video before upload
