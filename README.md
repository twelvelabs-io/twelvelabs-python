# TwelveLabs Python SDK

This SDK provides a convenient way to interact with the Twelve Labs Video Understanding Platform from an application written in the Python language. The SDK equips you with a set of intuitive classes and methods that streamline the process of interacting with the platform, minimizing the need for boilerplate code.


## Prerequisites

Ensure that the following prerequisites are met before using the SDK:

-  [Python](https://www.python.org) 3.7 or newer must be installed on your machine.
-  The API key of your account. If you don't have an account, please [sign up](https://api.twelvelabs.io/) for a free account. Then, to retrieve your API key, go to the [Dashboard](https://api.twelvelabs.io/dashboard) page, and select the **Copy** icon to the right of the key to copy it to your clipboard.

## Install the SDK

1. Clone the `twelvelabs-io/twelvelabs-python` GitHub repository:

    ```sh
    git clone https://github.com/twelvelabs-io/twelvelabs-python && cd twelvelabs-python
    ```

2. Install the `twelvelabs` package in editable mode:

    ```sh
    pip install -e .
    ```

3. _(Optional)_ By default, the SDK connects to the production environment. To use a different environment, set the `TWELVELABS_BASE_URL` environment variable by entering the following command and replacing `<YOUR_DEVELOPMENT_BASE_URL>` with the desired base URL:

    ```sh
    export TWELVELABS_BASE_URL=<YOUR_DEVELOPMENT_BASE_URL>
    ```

    The following example connects the SDK to the development environment:


    ```sh
    export TWELVELABS_BASE_URL=https://api.twelvelabs.space
    ```



## Initialize the SDK

1. Import the SDK into your application:

   ```py
   from twelvelabs import TwelveLabs
   ```

2.  Instantiate the SDK client with your API key. This example code assumes that your API key is stored in an environment variable named `TL_API_KEY`:

    ```py
    client = TwelveLabs(api_key=os.getenv('TL_API_KEY'))
    ```

## Use the SDK

To get started with the SDK, follow these basic steps:

1. Create an index.
2. Upload videos.
3. Perform downstream tasks, such as searching or generating text from video.

## Create an index

To create an index, use the example code below, replacing "<YOUR_INDEX_NAME>" with the desired name for your index:

```py
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

Note the following about this example:
- The platform provides two distinct engine types - embedding and generative, each serving unique purposes in multimodal video understanding.
  - **Embedding engines (Marengo)** : These engines are proficient at performing tasks such as search and classification, enabling enhanced video understanding.
  - **Generative engines (Pegasus)**: These engines generate text based on your videos.
  For your index, both Marengo and Pegasus are enabled.
- The `engines.options` fields specify the types of information each video understanding engine will process. For details, see the [Engine options](https://docs.twelvelabs.io/v1.2/docs/engine-options) page.

The output should look similar to the following:

```
Index(id='65b1b926560f741da96836d7', created_at='2024-01-25T01:28:06.061Z', updated_at='2024-01-25T01:28:06.061Z', name='test-index-to-researchers1', engines=[Engine(name='marengo2.5', options=['visual', 'conversation', 'text_in_video'], addons=None), Engine(name='pegasus1', options=['visual', 'conversation'], addons=None)], video_count=0, total_duration=0.0, expires_at='2024-04-24T01:28:06.061Z')
```

Note that the API returns, among other information, a field named `id`, representing the unique identifier of your new index.

For a description of each field in the request and response, see the [Create an index](https://docs.twelvelabs.io/v1.2/reference/create-index) page.


## Upload videos

Before you upload a video to the platform, ensure that it meets the following requirements:

- **Video resolution**: Must be greater or equal than 360p and less or equal than 4K. For consistent search results, Twelve Labs recommends you upload 360p videos.
- **Duration**: For Marengo, it must be between 4 seconds and 2 hours (7,200s). For Pegasus, it must be between 5 seconds and 30 minutes (1800s).
- **File size**: Must not exceed 2 GB. If you require different options, send us an email at support@twelvelabs.io.
- **Audio track**: If the `conversation` [engine option](https://docs.twelvelabs.io/v1.2/docs/engine-options) is selected, the video you're uploading must contain an audio track.

To upload a video, use the example code below, replacing the following:

- **`<YOUR_VIDEO_ID>`**: with a string representing the unique identifier of your video.
- **`<YOUR_VIDEO_PATH>`**: with a string representing the path to your video file.


```py
task = client.task.create(index_id="<YOUR_INDEX_ID>", file="<YOUR_VIDEO_PATH>", language="en")

print(f"Uploading {video_path} and waiting for the indexing process to be completed.")
print(f"Created task: id={task.id}, status={task.status}")

def on_task_update(task):
    print(f"  Status={task.status}")

task.wait_for_done(callback=on_task_update)

if task.status != "ready":
    raise RuntimeError(f"Indexing failed with status {task.status}")
print(f"Uploaded {video_path}")
```

Note that once the video has been successfully uploaded and indexed, the response `task` object will contain a field named `video_id`, representing the unique identifier of your video.

For a description of each field in the request and response, see the [Create a video indexing task](https://docs.twelvelabs.io/reference/create-video-indexing-task) page.

## Perform downstream tasks

The sections below show how you can perform the most common downstream tasks. See [our documentation](https://docs.twelvelabs.io/docs) for a complete list of all the features the Twelve Labs Understanding Platform provides.

### Search

To perform a search request, use the example code below, replacing the following:

- **`<YOUR_VIDEO_ID>`**: with a string representing the unique identifier of your video.
- **`<YOUR_QUERY>`**: with a string representing your search query. Note that the API supports full natural language-based search. The following examples are valid queries: "birds flying near a castle," "sun shining on water," and "an officer holding a child's hand."
- **`[<YOUR_SEARCH_OPTIONS>]`**: with an array of strings that specifies the sources of information the platform uses when performing a search. For example, to search based on visual and conversation cues, use `["visual", "conversation"]`. For details, see the [Search options](https://docs.twelvelabs.io/docs/search-options) page.

```py
result = client.search.query("<YOUR_VIDEO_ID>", "<YOUR_QUERY>", ["<YOUR_SEARCH_OPTIONS>"])
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

For a description of each field in the request and response, see the [Make a search request](https://docs.twelvelabs.io/v1.2/reference/make-search-request) page.

### Generate text from video

The Twelve Labs Video Understanding Platform offers three distinct endpoints tailored to meet various requirements. Each endpoint has been designed with specific levels of flexibility and customization to accommodate different needs.

Note the following about using these endpoints:
- The Pegasus video understanding engine must be enabled for the index to which your video has been uploaded.
- Your prompts must be instructive or descriptive, and you should not phrase them as questions.
- The maximum length of a prompt is 300 characters.

#### Topics, titles, and hashtags

To generate topics, titles, and hashtags, use the example code below, replacing the following:

- **`<YOUR_VIDEO_ID>`**: with a string representing the unique identifier of your video.
- **`[<TYPES>]`**: with an array of strings representing the type of text the platform should generate. Example: `["title", "topic", "hashtag"]`.

```py
gist = client.generate.gist("<YOUR_VIDEO_ID>", types=["<TYPES>"])
print(f"Title = {gist.title}\nTopics = {gist.topics}\nHashtags = {gist.hashtags}")
```

For a description of each field in the request and response, see the [Titles, topics, or hashtags](https://docs.twelvelabs.io/v1.2/reference/generate-gist) page.

#### Summaries, chapters, and highlights

To generate summaries, chapters, and highlights, use the example code below, replacing the following:

- **`<YOUR_VIDEO_ID>`**: with a string representing the unique identifier of your video.
- **`<TYPE>`**: with a string representing the type of text the platform should generate. This parameter can take one of the following values: "summary", "chapter", or "highlight".
- _(Optional)_ **`<YOUR_PROMPT>`**: with a string that provides context for the summarization task, such as the target audience, style, tone of voice, and purpose. Example:  "Generate a summary in no more than 5 bullet points."


```py
res = client.generate.summarize("<YOUR_VIDEO_ID>", type="<TYPE>", prompt="<YOUR_PROMPT>")
print(f"{res.summary}")
```

For a description of each field in the request and response, see the [Summaries, chapters, or highlights](https://docs.twelvelabs.io/v1.2/docs/generate-summaries-chapters-highlights) page.

#### Open-ended texts

To generate open-ended texts, use the example code below, replacing the following:
- **`<YOUR_VIDEO_ID>`**: with a string representing the unique identifier of your video.
- **`<YOUR_PROMPT>`**: with a string that guides the model on the desired format or content. The maximum length of the prompt is 500 tokens or roughly 350 words. Example:  "I want to generate a description for my video with the following format: Title of the video, followed by a summary in 2-3 sentences, highlighting the main topic, key events, and concluding remarks."

```py
res = client.generate.text(video_id="<YOUR_VIDEO_ID>", prompt="<YOUR_PROMPT>")
print(f"{res.data}")
```

## Error Handling

The SDK includes a set of exceptions that are mapped to specific HTTP status codes, as shown in the table below:

| Exception | HTTP Status Code |
|----------|----------|
| BadRequestError| 400 |
| AuthenticationError | 401 |
| PermissionDeniedError  | 403 |
| NotFoundError | 404 |
| ConflictError | 409 |
| UnprocessableEntityError | 422 |
| RateLimitError | 429 |
| InternalServerError | 5xx |

The following example shows how you can handle specific HTTP errors in your application:

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
    print("Bad request.")
except twelvelabs.APIStatusError as e:
    print(f"Status code {e.status_code} received")
    print(e.response)
```

## TODO

- cli
- validate video before upload
