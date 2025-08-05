# TwelveLabs Python SDK

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Ffern-demo%2Ftwelve-labs-python)
[![PyPI version](https://img.shields.io/pypi/v/twelvelabs.svg)](https://pypi.org/project/twelvelabs/)
![Pepy Total Downloads](https://img.shields.io/pepy/dt/twelvelabs)

> **NOTE**: This version includes breaking changes compared to the 0.4.x version. To use it in your application, you must update your code and thoroughly test the changes to ensure everything functions as expected before deploying it to production environments. If you want to use the legacy version, please refer to the [0.4 folder](./0.4).

This SDK provides a convenient way to interact with the Twelve Labs Video Understanding Platform from an application written in the Python language. The SDK equips you with a set of intuitive classes and methods that streamline the process of interacting with the platform, minimizing the need for boilerplate code.

# Prerequisites

Ensure that the following prerequisites are met before using the SDK:

- [Python](https://www.python.org) 3.7 or newer must be installed on your machine.
- You have an API key. If you don't have an account, please [sign up](https://playground.twelvelabs.io/) for a free account. Then, to retrieve your API key, go to the [API Key](https://playground.twelvelabs.io/dashboard/api-key) page, and select the **Copy** icon to the right of the key to copy it to your clipboard.

# Install the SDK

Install the latest version of the `twelvelabs` package:

```sh
pip install twelvelabs
```

# Initialize the SDK

1. Import the SDK into your application:

   ```py
   from twelvelabs import TwelveLabs
   ```

2. Instantiate the SDK client with your API key:

   ```py
   client = TwelveLabs(api_key="<YOUR_API_KEY>")
   ```

# Use the SDK

To get started with the SDK, follow these basic steps:

1. Create an index.
2. Upload videos.
3. Perform downstream tasks, such as searching or analyzing videos to generate text based on their content.

## Create an index

To create an index, use the example code below, replacing "<YOUR_INDEX_NAME>" with the desired name for your index:

```py
from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem

try:
    index = client.indexes.create(
        index_name="<YOUR_INDEX_NAME>",
        models=[
            IndexesCreateRequestModelsItem(
                model_name="marengo2.7",
                model_options=["visual", "audio"],
            ),
            IndexesCreateRequestModelsItem(
                model_name="pegasus1.2",
                model_options=["visual", "audio"],
            ),
        ],
    )
except Exception as e:
    print(f"Error: {e}")
print(f"Created index: id={index.id} name={index.name}")
```

Note the following about this example:

- The platform provides two distinct models, each serving unique purposes in multimodal video understanding.
  - **Marengo**: An embedding model that analyzes multiple modalities in video content, including visuals, audio, and text, to provide a holistic understanding similar to human comprehension. Key use cases include searching using image or natural-language queries and creating embeddings for various downstream applications. The current version is Marengo 2.7.
  - **Pegasus**: A generative model that analyzes multiple modalities to generate contextually relevant text based on the content of your videos. Key use cases include content summarization and timestamp identification. The current version is Pegasus 1.2.
    This example enables both Marengo and Pegasus.
- The `models.model_options` fields specify the modalities each video understanding model will process.
- The models and the model options specified when you create an index apply to all the videos you upload to that index and cannot be changed.

Note that the platform returns, among other information, a field named `id`, representing the unique identifier of your new index.

For a description of each field in the request and response, see the [Create an index](https://docs.twelvelabs.io/v1.3/sdk-reference/python/manage-indexes#create-an-index) section.

## Upload videos

Before you upload a video to the platform, ensure that it meets the following requirements:

- **Video resolution**: The shorter side (width or height) must be at least 360 pixels and must not exceed 2160 pixels.
- **Aspect ratio**: Must be one of the following (including both landscape and portrait variants): 1:1, 4:3, 4:5, 5:4, 16:9, 9:16, or 17:9.
- **Video and audio formats**: The video files you wish to upload must be encoded in the video and audio formats listed on the [FFmpeg Formats Documentation](https://ffmpeg.org/ffmpeg-formats.html) page. For videos in other formats, contact us at [support@twelvelabs.io](mailto:support@twelvelabs.io).
- **Duration**: For Marengo, it must be between 4 seconds and 2 hours (7,200s). For Pegasus, it must be between 4 seconds and 1 hour (3,600s).
- **File size**: Must not exceed 2 GB.

If you require different options, send us an email at support@twelvelabs.io.

To upload videos, use the example code below, replacing the following:

- **`<YOUR_VIDEO_PATH>`**: with a string representing the path to the directory containing the video files you wish to upload.
- **`<YOUR_INDEX_ID>`**: with a string representing the unique identifier of the index to which you want to upload your video.

```py
from glob import glob

video_files = glob("<YOUR_VIDEO_PATH>") # Example: "/videos/*.mp4"
for video_file in video_files:
  print(f"Uploading {video_file}")
  task = client.tasks.create(index_id="<YOUR_INDEX_ID>", video_file=video_file)
  print(f"Task id={task.id}")

  task.wait_for_done(sleep_interval=5, callback=lambda t: print(f"  Status={t.status}"))
  if task.status != "ready":
      raise RuntimeError(f"Indexing failed with status {task.status}")
  print(f"Upload complete. The unique identifier of your video is {task.video_id}.")
```

For a description of each field in the request and response, see the [Create a video indexing task](https://docs.twelvelabs.io/v1.3/sdk-reference/python/upload-videos#create-a-video-indexing-task) section.

## Perform downstream tasks

The sections below show how you can perform the most common downstream tasks. See [our documentation](https://docs.twelvelabs.io/docs) for a complete list of all the features the Twelve Labs Understanding Platform provides.

### Search

To search for relevant video content, you can use either text or images as queries:

- **Text queries**: Use natural language to find video segments matching specific keywords or phrases.
- **Image queries**: Use images to find video segments that are semantically similar to the provided images.

**Search using text queries**

To perform a search request using text queries, use the example code below, replacing the following:

- **`<YOUR_INDEX_ID>`**: with a string representing the unique identifier of your index.
- **`<YOUR_QUERY>`**: with a string representing your search query. Note that the API supports full natural language-based search. The following examples are valid queries: "birds flying near a castle," "sun shining on water," and "an officer holding a child's hand."
- **`[<YOUR_SEARCH_OPTIONS>]`**: with an array of strings that specifies the modalities the platform uses when performing a search. For example, to search based on visual and audio cues, use `["visual", "audio"]`. Note that the search options you specify must be a subset of the model options used when you created the index. For more details, see the [Search options](https://docs.twelvelabs.io/v1.3/docs/concepts/modalities#search-options) section.

```py
search_results = client.search.query(
    index_id=index.id,
    query_text="<YOUR_QUERY>",
    options=["visual", "audio"]
    )
for clip in search_results.data:
    print(f" video_id={clip.video_id} score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}")
```

Note that the response contains, among other information, the following fields:

- `video_id`: The unique identifier of the video that matched your search terms.
- `score`: A quantitative value determined by the AI model representing the level of confidence that the results match your search terms.
- `start`: The start time of the matching video clip, expressed in seconds.
- `end`: The end time of the matching video clip, expressed in seconds.
- `confidence`: A qualitative indicator based on the value of the score field. This field can take one of the following values:
  - `high`
  - `medium`
  - `low`

For a description of each field in the request and response, see the [Make a search request](https://docs.twelvelabs.io/v1.3/sdk-reference/python/search#make-a-search-request) page.

**Search using image queries**

You can provide images as local files or publicly accessible URLs. Use the `query_media_file` parameter for local image files and the `query_media_url` parameter for publicly accessible URLs.

To perform a search request using image queries, use the example code below, replacing the following:

- **`<YOUR_INDEX_ID>`**: with a string representing the unique identifier of your index.
- **`<YOUR_FILE_PATH>`**: with a string representing the path of the image file you wish to provide.
- **`[<YOUR_SEARCH_OPTIONS>]`**: with an array of strings that specifies the sources of information the platform uses when performing a search. For example, to search based on visual cues, use `["visual"]`. Note that the search options you specify must be a subset of the model options used when you created the index. For more details, see the [Search options](https://docs.twelvelabs.io/v1.3/docs/concepts/modalities#search-options) section.

```python
search_results = client.search.query(
    index_id="<YOUR_INDEX_ID>",
    query_media_type="image",
    query_media_file="<YOUR_FILE_PATH>",
    search_options=["<YOUR_SEARCH_OPTIONS>"]
)
```

The response is similar to that received when using text queries.

### Analyze videos

The Analyze API suite uses a multimodal approach to analyze videos and generate text, processing visuals, sounds, spoken words, and texts to provide a comprehensive understanding.

The Analyze API offers three distinct endpoints tailored to meet various requirements. Each endpoint has been designed with specific levels of flexibility and customization to accommodate different needs.

Note the following about using these endpoints:

- The Pegasus video understanding model must be enabled for the index to which your video has been uploaded.
- Your prompts must be instructive or descriptive, and you can also phrase them as questions.
- The maximum length of a prompt is 2,000 tokens.

#### Titles, topics, and hashtags

To analyze videos and generate titles, topics, and hashtags use the example code below, replacing the following:

- **`<YOUR_VIDEO_ID>`**: with a string representing the unique identifier of your video.

```py
from twelvelabs import TwelveLabs
gist = client.gist(video_id=task.video_id, types=["title", "topic", "hashtag"])
print(f"Title={gist.title}\nTopics={gist.topics}\nHashtags={gist.hashtags}")
```

#### Summaries, chapters, and highlights

To analyze videos and generate summaries, chapters, and highlights, use the example code below, replacing the following:

- **`<YOUR_VIDEO_ID>`**: with a string representing the unique identifier of your video.
- **`<TYPE>`**: with a string representing the type of text the platform should generate. This parameter can take one of the following values: "summary", "chapter", or "highlight".
- _(Optional)_ **`<YOUR_PROMPT>`**: with a string that provides context for the summarization task, such as the target audience, style, tone of voice, and purpose. Example: "Generate a summary in no more than 5 bullet points."

```py
res = client.summarize(video_id="<YOUR_VIDEO_ID>", type="<TYPE>", prompt="<YOUR_PROMPT>")
if res.summarize_type == "summary":
    print(f"{res.summary}")
elif res.summarize_type == "chapter":
    print(f"Chapters: {res.chapters}")
elif res.summarize_type == "highlight":
    print(f"Highlights: {res.highlights}")
```

For a description of each field in the request and response, see the [Summaries, chapters, or highlights](https://docs.twelvelabs.io/v1.3/sdk-reference/python/analyze-videos#summaries-chapters-and-highlights) page.

#### Open-ended analysis

To perform open-ended analysis and generate tailored text outputs based on your prompts, use the example code below, replacing the following:

- **`<YOUR_VIDEO_ID>`**: with a string representing the unique identifier of your video.
- **`<YOUR_PROMPT>`**: with a string that guides the model on the desired format or content. The maximum length of the prompt is 2,000 tokens. Example: "I want to generate a description for my video with the following format: Title of the video, followed by a summary in 2-3 sentences, highlighting the main topic, key events, and concluding remarks."
-
```py
res = client.analyze(video_id="<YOUR_VIDEO_ID>", prompt="<YOUR_PROMPT>")
print(f"{res.data}")
```

## Error Handling

The SDK includes a set of exceptions that are mapped to specific HTTP status codes, as shown in the table below:

| Exception                | HTTP Status Code |
| ------------------------ | ---------------- |
| BadRequestError          | 400              |
| AuthenticationError      | 401              |
| PermissionDeniedError    | 403              |
| NotFoundError            | 404              |
| ConflictError            | 409              |
| UnprocessableEntityError | 422              |
| RateLimitError           | 429              |
| InternalServerError      | 5xx              |

The following example shows how you can handle specific HTTP errors in your application:

```python
import os
from twelvelabs import TwelveLabs
from twelvelabs.errors import BadRequestError, NotFoundError

client = TwelveLabs(api_key=os.getenv("TWELVELABS_API_KEY"))
try:
    indexes = client.indexes.list()
    print(indexes)
except BadRequestError as e:
    print("Bad request.")
except NotFoundError as e:
    print("Not found.")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Contributing

This repository contains code that has been automatically generated from an OpenAPI specification. We are unable to merge direct code contributions to the SDK because the code generation tool overwrites manual changes with each new release.

To contribute, follow these steps:

1. Open an issue to discuss your proposed changes with our team.
2. If you would like to submit a proof of concept, create a pull request. We will review your pull request, but we cannot merge it.
3. We will transfer any approved changes to the repository where the code generation tool operates.

We welcome contributions to the README file. You can submit pull requests directly.
