# TwelveLabs Python SDK

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Ffern-demo%2Ftwelve-labs-python)
[![PyPI version](https://img.shields.io/pypi/v/twelvelabs.svg)](https://pypi.org/project/twelvelabs/)
![Pepy Total Downloads](https://img.shields.io/pepy/dt/twelvelabs)

The TwelveLabs Python SDK provides a set of intuitive classes and methods that streamline platform interaction, minimizing the need for boilerplate code.

> **Note**: The examples in this guide show only the required parameters. For the complete guides, see the [Search](https://docs.twelvelabs.io/docs/guides/search) and [Analyze videos](https://docs.twelvelabs.io/docs/guides/analyze-videos) pages.

# Prerequisites

Ensure that the following prerequisites are met before using the SDK:

- [Python](https://www.python.org) 3.7 or newer must be installed on your machine.
- To use the platform, you need an API key:
  1. If you don't have an account, [sign up](https://playground.twelvelabs.io/) for a free account.
  2. Go to the [API Keys](https://playground.twelvelabs.io/dashboard/api-keys) page.
  3. If you need to create a new key, select the **Create API Key** button. Enter a name and set the expiration period. The default is 12 months.
  4. Select the **Copy** icon next to your key to copy it to your clipboard.
- Your video files must meet the following requirements:
    - **For this guide**: Files up to 4 GB.
    - **Model capabilities**: See the complete requirements for [Marengo](https://docs.twelvelabs.io/v1.3/docs/concepts/models/marengo#video-file-requirements) and [Pegasus](https://docs.twelvelabs.io/v1.3/docs/concepts/models/pegasus#video-file-requirements) for resolution, aspect ratio, and supported formats.
    
    For upload size limits and processing modes, see the [Upload and processing methods](https://docs.twelvelabs.io/v1.3/docs/concepts/upload-methods) page.

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

Indexes store and organize your video data, allowing you to group related videos. When you create an index, configure which video understanding models process your videos and what modalities those models analyze.

To create an index, call the `client.indexes.create` method with the following parameters:

- **`index_name`**: The name of the index.
- **`models`**: An array of models to enable. Each entry has two fields:
  - **`model_name`**: The model to enable. Use `"marengo3.0"` for search or `"pegasus1.2"` for text generation.
  - **`model_options`**: The modalities to analyze.

```py
index = client.indexes.create(
    index_name="<YOUR_INDEX_NAME>",
    models=[
        {"model_name": "marengo3.0", "model_options": ["visual", "audio"]},
        {"model_name": "pegasus1.2", "model_options": ["visual", "audio"]}
    ]
)
if not index.id:
    raise RuntimeError("Failed to create an index.")
print(f"Created index: id={index.id}")
```

The `client.indexes.create` method returns an object that includes, among other information, a field named `id` representing the unique identifier of your new index.

See the [Indexes](https://docs.twelvelabs.io/docs/concepts/indexes) page for more details.

## Upload videos

To upload a video, call the `client.assets.create` method with the following parameters:

- **`method`**: Upload method. Use `"url"` for publicly accessible URLs or `"direct"` for local files.
- **`url`** or **`file`**: The video URL or an opened file object in binary read mode. Use direct links to raw media files. Hosting platform links and cloud storage sharing links are not supported.

```py
asset = client.assets.create(
    method="url",
    url="<YOUR_VIDEO_URL>"
    # Or use method="direct" and file=open("<PATH_TO_VIDEO_FILE>", "rb") to upload a local file.
)
print(f"Created asset: id={asset.id}")
```

The `client.assets.create` method returns an object that includes, among other information, a field named `id` representing the unique identifier of your asset. Use this identifier in subsequent steps.

## Check the status of the asset

You only need this step for files larger than 200 MB. The platform processes files up to 200 MB synchronously and sets the asset status to ready. For larger files, check the asset status until it is ready.

To check the status of the asset, call the `client.assets.retrieve` method with the unique identifier of your asset as a paremeter:

```py
print("Waiting for asset to be ready...")
while True:
    asset = client.assets.retrieve(asset.id)
    if asset.status == "ready":
        print("Asset is ready")
        break
    if asset.status == "failed":
        raise RuntimeError(f"Asset processing failed: id={asset.id}")
    time.sleep(5)
```

## Index your video

To index your video, call the `client.indexes.indexed_assets.create` method with the following parameters:

- **`index_id`**: The unique identifier of your index.
- **`asset_id`**: The unique identifier of the asset to index.

```py
indexed_asset = client.indexes.indexed_assets.create(
    index_id=index.id,
    asset_id=asset.id
)
print(f"Created indexed asset: id={indexed_asset.id}")
```

The `client.indexes.indexed_assets.create` method returns an object that includes, among other information, a field named `id` representing the unique identifier of your indexed asset.

## Monitor the indexing process

The platform indexes videos asynchronously. To monitor the indexing process, call the `client.indexes.indexed_assets.retrieve` method with the following parameters:

- **`index_id`**: The unique identifier of your index.
- **`indexed_asset_id`**: The unique identifier of your indexed asset.

```py
import time

print("Waiting for indexing to complete.")
while True:
    indexed_asset = client.indexes.indexed_assets.retrieve(
        index_id=index.id,
        indexed_asset_id=indexed_asset.id
    )
    print(f"  Status={indexed_asset.status}")
    if indexed_asset.status == "ready":
        print("Indexing complete!")
        break
    elif indexed_asset.status == "failed":
        raise RuntimeError("Indexing failed")
    time.sleep(5)
```

The `client.indexes.indexed_assets.retrieve` method returns an object that includes, among other information, a field named `status` representing the status of the indexing process. Poll this method until `status` is `"ready"` before performing downstream tasks.

## Perform downstream tasks

The sections below show the most common downstream tasks. See [our documentation](https://docs.twelvelabs.io/docs) for the complete list of features the platform provides.

### Search

Use natural language, images, or both to find matching video segments. Search operates within a single index.

**Text queries**

To search using a text query, call the `client.search.query` method with the following parameters:

- **`query_text`**: Natural language query. The maximum length of a query is 500 tokens.
- **`search_options`**: Modalities to search. Valid values: `"visual"`, `"audio"`, `"transcription"` (spoken words). See the [Search options](https://docs.twelvelabs.io/docs/concepts/modalities#search-options) page for details.

```py
search_results = client.search.query(
    index_id=index.id,
    query_text="<YOUR_QUERY>",
    search_options=["visual", "audio"]
)
for i, clip in enumerate(search_results):
    print(f"Result {i + 1}: video_id={clip.video_id} rank={clip.rank} start={clip.start}s end={clip.end}s")
```

The `client.search.query` method returns an iterable where each item contains, among other information, the following fields:

- `video_id`: The unique identifier of the matching video.
- `rank`: The relevance ranking (1 = most relevant).
- `start`, `end`: The start and end time of the matching clip, expressed in seconds.

**Image queries**

To search using an image query, call the `client.search.query` method with the following parameters:

- **`query_media_type`**: Must be `"image"`.
- **`query_media_file`**, **`query_media_url`**, **`query_media_files`**, or **`query_media_urls`**: The image or images to use as a query (up to 10 total). Provide at least one of the following:
  - _(Optional)_ **`query_media_file`**: An opened file object in binary read mode.
  - _(Optional)_ **`query_media_url`**: The publicly accessible URL of your image file.
  - _(Optional)_ **`query_media_files`**: A list of opened file objects in binary read mode.
  - _(Optional)_ **`query_media_urls`**: A list of publicly accessible URLs.

```py
search_results = client.search.query(
    index_id=index.id,
    query_media_type="image",
    query_media_url="<YOUR_IMAGE_URL>",
    # Or use query_media_file=open("<PATH_TO_IMAGE_FILE>", "rb") for a local file.
    # Or use query_media_urls=["<URL_1>", "<URL_2>"] for multiple URLs.
    # Or use query_media_files=[open("<FILE_1>", "rb"), open("<FILE_2>", "rb")] for multiple local files.
    search_options=["visual"]
)
for i, clip in enumerate(search_results):
    print(f"Result {i + 1}: video_id={clip.video_id} rank={clip.rank} start={clip.start}s end={clip.end}s")
```

The response is similar to that received when using text queries.

**Composed queries**

Combine up to 10 images with text to narrow results. For example, provide an image of a car and add "red color" to find only red instances of that vehicle.

To perform a composed query, call the `client.search.query` method with the following parameters:

- **`query_media_file`**, **`query_media_url`**, **`query_media_files`**, or **`query_media_urls`**: The image or images to use as a query (up to 10 total). Provide at least one of the following:
  - _(Optional)_ **`query_media_file`**: An opened file object in binary read mode.
  - _(Optional)_ **`query_media_url`**: The publicly accessible URL of your image file.
  - _(Optional)_ **`query_media_files`**: A list of opened file objects in binary read mode.
  - _(Optional)_ **`query_media_urls`**: A list of publicly accessible URLs.
- **`query_text`**: Text that refines the image query.

```py
search_results = client.search.query(
    index_id=index.id,
    query_media_type="image",
    query_media_url="<YOUR_IMAGE_URL>",
    # Or use query_media_file=open("<PATH_TO_IMAGE_FILE>", "rb") for a local file.
    # Or use query_media_urls=["<URL_1>", "<URL_2>"] for multiple URLs.
    # Or use query_media_files=[open("<FILE_1>", "rb"), open("<FILE_2>", "rb")] for multiple local files.
    query_text="<YOUR_QUERY>",
    search_options=["visual"]
)
for i, clip in enumerate(search_results):
    print(f"Result {i + 1}: video_id={clip.video_id} rank={clip.rank} start={clip.start}s end={clip.end}s")
```

The response is similar to that received when using text queries.

### Analyze videos

The platform uses a multimodal approach to analyze video content, processing visuals, sounds, spoken words, and on-screen text. Use a custom prompt to generate summaries, extract insights, answer questions, or produce structured output.

Note the following about using these methods:

- The Pegasus model must be enabled for the index.
- Your prompts can be instructive or descriptive, or you can phrase them as questions.
- The maximum length of a prompt is 2,000 tokens.

**Streaming responses**

Streaming delivers text fragments in real-time. Use it for live transcription or when you need immediate output.

To analyze a video with streaming responses, call the `client.analyze_stream` method with the following parameters:

- **`video_id`**: The unique identifier of the indexed asset.
- **`prompt`**: Guides text generation, and it can be instructive, descriptive, or a question. The maximum length is 2,000 tokens.

```py
text_stream = client.analyze_stream(
    video_id=indexed_asset.id,
    prompt="<YOUR_PROMPT>"
)
for text in text_stream:
    if text.event_type == "text_generation":
        print(text.text)
```

The `client.analyze_stream` method returns a stream of objects. The `event_type` field can be `"stream_start"`, `"text_generation"`, or `"stream_end"`.

**Non-streaming responses**

Non-streaming returns the complete text in a single response. Use it for reports or summaries where you need the full result at once. Call the `client.analyze` method with the same parameters as `client.analyze_stream`.

```py
result = client.analyze(
    video_id=indexed_asset.id,
    prompt="<YOUR_PROMPT>"
)
print(result.data)
```

The `client.analyze` method returns an object where the `data` field contains the complete generated text string (up to 4,096 tokens).

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

```py
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
