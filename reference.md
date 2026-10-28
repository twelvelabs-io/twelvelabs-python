# Reference
<details><summary><code>client.<a href="src/twelvelabs/base_client.py">analyze_stream</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method analyzes a video or one or more images and returns the results directly in the response. Each request must contain a video or one or more images, but not both. You can use general analysis (prompt-based text generation) with either media type.

<Accordion title="Input requirements">
**Videos**
- Minimum duration: 1 second
- Maximum duration: 1 hour
- Formats: [FFmpeg supported formats](https://ffmpeg.org/ffmpeg-formats.html)
- Resolution: 360x360 to 5184x2160 pixels
- Aspect ratio: Between 1:1 and 1:2.4, or between 2.4:1 and 1:1.

**Images**
- You can provide one to twenty images per request.
- Formats: JPEG, PNG, WebP, GIF, and BMP.
- Maximum size: 20 MB per image.
- Maximum pixel count: 16,777,216 pixels per image (width × height).
</Accordion>

**When to use this method**:
- Analyze videos up to 1 hour, or analyze images
- Retrieve immediate results without polling for task completion
- Stream text fragments in real time for immediate processing and feedback

**Do not use this method for**:
- Videos longer than 1 hour. Use the [`POST`](/v1.3/api-reference/analyze-videos/create-async-analysis-task) method of the `/analyze/tasks` endpoint instead.
- Video segmentation with custom segment definitions. Use the [`POST`](/v1.3/api-reference/analyze-videos/create-async-analysis-task) method of the `/analyze/tasks` endpoint instead.

On the Free plan, you have a total of 600 minutes (10 hours) shared across indexing, analysis, and segmentation. For details, see the [Video hours and video count limits](/v1.3/docs/concepts/indexes#video-hours-and-video-count-limits) section.

<Note title="Note">
This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.analyze_stream()
for chunk in response:
    print(chunk)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_name:** `typing.Optional[AnalyzeStreamRequestModelName]` 

The video understanding model to use for analysis.
- `pegasus1.6`: For details about this version, see the [Pegasus 1.6](/v1.3/docs/concepts/models/pegasus/pegasus-1-6) page.
- `pegasus1.5`: For details about this version, see the [Pegasus 1.5](/v1.3/docs/concepts/models/pegasus/pegasus-1-5) page.

**Default:** `pegasus1.5`
    
</dd>
</dl>

<dl>
<dd>

**video:** `typing.Optional[VideoContext]` 
    
</dd>
</dl>

<dl>
<dd>

**image:** `typing.Optional[typing.Sequence[AnalyzeImageInput]]` 

A list of up to twenty objects containing the images to analyze. For each image, include exactly one source. Requires Pegasus 1.6. Using any other model returns a `parameter_invalid` error.

Mutually exclusive with the `video` and `prompt_v2` parameters. The `prompt` parameter is required when you provide images.
    
</dd>
</dl>

<dl>
<dd>

**prompt:** `typing.Optional[AnalyzeTextPrompt]` 

A text prompt that guides the model on the desired format or content. To include reference images in your prompt, use the `prompt_v2` parameter instead. Mutually exclusive with the `prompt_v2` parameter.

Your prompts can be instructive or descriptive, or you can phrase them as questions. This text counts toward the [context window](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#context-window).
    
</dd>
</dl>

<dl>
<dd>

**prompt_v_2:** `typing.Optional[AnalyzePromptV2]` 

A structured prompt that uses `<@name>` placeholders to reference images. Mutually exclusive with the `prompt` and `image` parameters.

The prompt text and reference images count toward the [context window](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#context-window).
    
</dd>
</dl>

<dl>
<dd>

**temperature:** `typing.Optional[AnalyzeTemperature]` 
    
</dd>
</dl>

<dl>
<dd>

**response_format:** `typing.Optional[SyncResponseFormat]` — Specifies the format of the response. When you omit this parameter, the platform returns unstructured text. Only the `json_schema` type is supported for synchronous analysis.
    
</dd>
</dl>

<dl>
<dd>

**max_tokens:** `typing.Optional[int]` — The maximum response length, in tokens.
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `typing.Optional[float]` 

Start of the analysis window, as an absolute timestamp in seconds, based on the internal metadata of the video. Use with `end_time` to analyze only a portion of the video.

<Note title="Notes">
- If omitted, defaults to the internal start time of the video.
- Most videos start at 0, but some (for example, from cameras or broadcast recordings) may have a non-zero start time. To find the value, run `ffprobe -v error -show_entries format=start_time,duration -of default=noprint_wrappers=1 your_video.mp4`.
- Must be less than `end_time` and the video duration. The window (`end_time - start_time`) must be at least 1 second.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[float]` 

End of the analysis window, as an absolute timestamp in seconds, based on the internal metadata of the video. Use with `start_time` to analyze only a portion of the video.

<Note title="Notes">
- If omitted, defaults to the internal start time of the video plus its duration.
- Most videos start at 0, but some (for example, from cameras or broadcast recordings) may have a non-zero start time. To find the value, run `ffprobe -v error -show_entries format=start_time,duration -of default=noprint_wrappers=1 your_video.mp4`.
- Must be greater than `start_time` and less than or equal to the video duration. The window (`end_time - start_time`) must be at least 1 second.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="src/twelvelabs/base_client.py">analyze</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method analyzes a video or one or more images and returns the results directly in the response. Each request must contain a video or one or more images, but not both. You can use general analysis (prompt-based text generation) with either media type.

<Accordion title="Input requirements">
**Videos**
- Minimum duration: 1 second
- Maximum duration: 1 hour
- Formats: [FFmpeg supported formats](https://ffmpeg.org/ffmpeg-formats.html)
- Resolution: 360x360 to 5184x2160 pixels
- Aspect ratio: Between 1:1 and 1:2.4, or between 2.4:1 and 1:1.

**Images**
- You can provide one to twenty images per request.
- Formats: JPEG, PNG, WebP, GIF, and BMP.
- Maximum size: 20 MB per image.
- Maximum pixel count: 16,777,216 pixels per image (width × height).
</Accordion>

**When to use this method**:
- Analyze videos up to 1 hour, or analyze images
- Retrieve immediate results without polling for task completion
- Stream text fragments in real time for immediate processing and feedback

**Do not use this method for**:
- Videos longer than 1 hour. Use the [`POST`](/v1.3/api-reference/analyze-videos/create-async-analysis-task) method of the `/analyze/tasks` endpoint instead.
- Video segmentation with custom segment definitions. Use the [`POST`](/v1.3/api-reference/analyze-videos/create-async-analysis-task) method of the `/analyze/tasks` endpoint instead.

On the Free plan, you have a total of 600 minutes (10 hours) shared across indexing, analysis, and segmentation. For details, see the [Video hours and video count limits](/v1.3/docs/concepts/indexes#video-hours-and-video-count-limits) section.

<Note title="Note">
This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_name:** `typing.Optional[AnalyzeRequestModelName]` 

The video understanding model to use for analysis.
- `pegasus1.6`: For details about this version, see the [Pegasus 1.6](/v1.3/docs/concepts/models/pegasus/pegasus-1-6) page.
- `pegasus1.5`: For details about this version, see the [Pegasus 1.5](/v1.3/docs/concepts/models/pegasus/pegasus-1-5) page.

**Default:** `pegasus1.5`
    
</dd>
</dl>

<dl>
<dd>

**video:** `typing.Optional[VideoContext]` 
    
</dd>
</dl>

<dl>
<dd>

**image:** `typing.Optional[typing.Sequence[AnalyzeImageInput]]` 

A list of up to twenty objects containing the images to analyze. For each image, include exactly one source. Requires Pegasus 1.6. Using any other model returns a `parameter_invalid` error.

Mutually exclusive with the `video` and `prompt_v2` parameters. The `prompt` parameter is required when you provide images.
    
</dd>
</dl>

<dl>
<dd>

**prompt:** `typing.Optional[AnalyzeTextPrompt]` 

A text prompt that guides the model on the desired format or content. To include reference images in your prompt, use the `prompt_v2` parameter instead. Mutually exclusive with the `prompt_v2` parameter.

Your prompts can be instructive or descriptive, or you can phrase them as questions. This text counts toward the [context window](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#context-window).
    
</dd>
</dl>

<dl>
<dd>

**prompt_v_2:** `typing.Optional[AnalyzePromptV2]` 

A structured prompt that uses `<@name>` placeholders to reference images. Mutually exclusive with the `prompt` and `image` parameters.

The prompt text and reference images count toward the [context window](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#context-window).
    
</dd>
</dl>

<dl>
<dd>

**temperature:** `typing.Optional[AnalyzeTemperature]` 
    
</dd>
</dl>

<dl>
<dd>

**response_format:** `typing.Optional[SyncResponseFormat]` — Specifies the format of the response. When you omit this parameter, the platform returns unstructured text. Only the `json_schema` type is supported for synchronous analysis.
    
</dd>
</dl>

<dl>
<dd>

**max_tokens:** `typing.Optional[int]` — The maximum response length, in tokens.
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `typing.Optional[float]` 

Start of the analysis window, as an absolute timestamp in seconds, based on the internal metadata of the video. Use with `end_time` to analyze only a portion of the video.

<Note title="Notes">
- If omitted, defaults to the internal start time of the video.
- Most videos start at 0, but some (for example, from cameras or broadcast recordings) may have a non-zero start time. To find the value, run `ffprobe -v error -show_entries format=start_time,duration -of default=noprint_wrappers=1 your_video.mp4`.
- Must be less than `end_time` and the video duration. The window (`end_time - start_time`) must be at least 1 second.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[float]` 

End of the analysis window, as an absolute timestamp in seconds, based on the internal metadata of the video. Use with `start_time` to analyze only a portion of the video.

<Note title="Notes">
- If omitted, defaults to the internal start time of the video plus its duration.
- Most videos start at 0, but some (for example, from cameras or broadcast recordings) may have a non-zero start time. To find the value, run `ffprobe -v error -show_entries format=start_time,duration -of default=noprint_wrappers=1 your_video.mp4`.
- Must be greater than `start_time` and less than or equal to the video duration. The window (`end_time - start_time`) must be at least 1 second.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Tasks
<details><summary><code>client.tasks.<a href="src/twelvelabs/tasks/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Info>This method will be removed in a future version.</Info>

This method returns a list of the video indexing tasks in your account. The platform returns your video indexing tasks sorted by creation date, with the newest at the top of the list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.tasks.list(
    page=1,
    page_limit=10,
    sort_by="created_at",
    sort_option="desc",
    index_id="630aff993fcee0532cb809d0",
    status=["ready", "failed"],
    filename="01.mp4",
    duration=531.998133,
    width=640,
    height=360,
    created_at="2024-03-01T00:00:00Z",
    updated_at="2024-03-01T00:00:00Z",
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[str]` 

The field to sort on. The following options are available:
- `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was updated.
- `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was created.

**Default**: `created_at`.
    
</dd>
</dl>

<dl>
<dd>

**sort_option:** `typing.Optional[str]` 

The sorting direction. The following options are available:
- `asc`
- `desc`

**Default**: `desc`.
    
</dd>
</dl>

<dl>
<dd>

**index_id:** `typing.Optional[str]` — Filter by the unique identifier of an index.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[
    typing.Union[
        TasksListRequestStatusItem, typing.Sequence[TasksListRequestStatusItem]
    ]
]` 

Filter by one or more video indexing task statuses. The following options are available:
- `ready`: The video has been successfully uploaded and indexed.
- `uploading`: The video is being uploaded.
- `validating`: The video is being validated against the prerequisites.
- `pending`: The video is pending.
- `queued`: The video is queued.
- `indexing`: The video is being indexed.
- `failed`: The video indexing task failed.

To filter by multiple statuses, specify the `status` parameter for each value:
```
status=ready&status=validating
```
    
</dd>
</dl>

<dl>
<dd>

**filename:** `typing.Optional[str]` — Filter by filename.
    
</dd>
</dl>

<dl>
<dd>

**duration:** `typing.Optional[float]` — Filter by duration. Expressed in seconds.
    
</dd>
</dl>

<dl>
<dd>

**width:** `typing.Optional[int]` — Filter by width.
    
</dd>
</dl>

<dl>
<dd>

**height:** `typing.Optional[int]` — Filter by height.
    
</dd>
</dl>

<dl>
<dd>

**created_at:** `typing.Optional[str]` — Filter video indexing tasks by the creation date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the video indexing tasks that were created on the specified date at or after the given time.
    
</dd>
</dl>

<dl>
<dd>

**updated_at:** `typing.Optional[str]` — Filter video indexing tasks by the last update date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the video indexing tasks that were updated on the specified date at or after the given time.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tasks.<a href="src/twelvelabs/tasks/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>


<Info>This method will be removed in a future version. New implementations should use [direct](/v1.3/api-reference/upload-content/direct-uploads) or [multipart](/v1.3/api-reference/upload-content/multipart-uploads) uploads followed by [separate indexing](/v1.3/api-reference/index-content/create).</Info>

This method creates a video indexing task that uploads and indexes a video in a single operation.

<Note title="Adding videos to existing indexes">
You can no longer add videos to an index that has only Pegasus 1.2 enabled. When you add videos to an index that has both Marengo and Pegasus 1.2 enabled, the platform indexes them with Marengo only.
</Note>

Upload options:
- **Local file**: Use the `video_file` parameter.
- **Publicly accessible URL**: Use the `video_url` parameter.

Your videos must meet requirements based on your workflow:
- **Search**: [Marengo requirements](/v1.3/docs/concepts/models/marengo/marengo-3-0#video-file-requirements).
- **Video analysis**: [Pegasus requirements](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#video-file-requirements).
- If you want to both search and analyze your videos, the most restrictive requirements apply.
- This method allows you to upload files up to 2 GB in size. To upload larger files, use the [Multipart Upload API](/v1.3/api-reference/upload-content/multipart-uploads)

Indexes have limits on video hours and video count. For details, see the [Video hours and video count limits](/v1.3/docs/concepts/indexes#video-hours-and-video-count-limits) section.

<Note title="Note">
This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.tasks.create(
    index_id="index_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index to which the video is being uploaded.
    
</dd>
</dl>

<dl>
<dd>

**video_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**video_url:** `typing.Optional[str]` — Specify this parameter to upload a video from a publicly accessible URL.
    
</dd>
</dl>

<dl>
<dd>

**enable_video_stream:** `typing.Optional[bool]` — This parameter indicates if the platform stores the video for streaming. When set to `true`, the platform stores the video, and you can retrieve its URL by calling the [`GET`](/v1.3/api-reference/videos/retrieve) method of the `/indexes/{index-id}/videos/{video-id}` endpoint. You can then use this URL to access the stream over the <a href="https://en.wikipedia.org/wiki/HTTP_Live_Streaming" target="_blank">HLS</a> protocol.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `typing.Optional[str]` — Metadata that helps you categorize your videos. You can specify a list of keys and values. Keys are strings, and values can be a string, a number, a boolean, or an array of strings. Send an integer wider than 53 bits (-9007199254740991 to 9007199254740991), and any identifier you want preserved verbatim, as a string. Send this value as a JSON-encoded string.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tasks.<a href="src/twelvelabs/tasks/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Info>This method will be removed in a future version.</Info>

This method retrieves a video indexing task.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.tasks.retrieve(
    task_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**task_id:** `str` — The unique identifier of the video indexing task to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tasks.<a href="src/twelvelabs/tasks/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Info>This method will be removed in a future version.</Info>

This action cannot be undone.
Note the following about deleting a video indexing task:
- You can only delete video indexing tasks for which the status is `ready` or `failed`.
- If the status of your video indexing task is `ready`, you must first delete the video vector associated with your video indexing task by calling the [`DELETE`](/v1.3/api-reference/videos/delete) method of the `/indexes/videos` endpoint.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.tasks.delete(
    task_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**task_id:** `str` — The unique identifier of the video indexing task you want to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Indexes
<details><summary><code>client.indexes.<a href="src/twelvelabs/indexes/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of the indexes in your account. The platform returns indexes sorted by creation date, with the oldest indexes at the top of the list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.indexes.list(
    page=1,
    page_limit=10,
    sort_by="created_at",
    sort_option="desc",
    index_name="myIndex",
    model_options="visual,audio",
    model_family="marengo",
    created_at="2024-08-16T16:53:59Z",
    updated_at="2024-08-16T16:55:59Z",
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[str]` 

The field to sort on. The following options are available:
- `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was updated.
- `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was created.

**Default**: `created_at`.
    
</dd>
</dl>

<dl>
<dd>

**sort_option:** `typing.Optional[str]` 

The sorting direction. The following options are available:
- `asc`
- `desc`

**Default**: `desc`.
    
</dd>
</dl>

<dl>
<dd>

**index_name:** `typing.Optional[str]` — Filter by the name of an index.
    
</dd>
</dl>

<dl>
<dd>

**model_options:** `typing.Optional[str]` — Filter by the model options. When filtering by multiple model options, the values must be comma-separated.
    
</dd>
</dl>

<dl>
<dd>

**model_family:** `typing.Optional[str]` — Filter by the model family. This parameter can take one of the following values: `marengo` or `pegasus`. You can specify a single value.
    
</dd>
</dl>

<dl>
<dd>

**created_at:** `typing.Optional[str]` — Filter indexes by the creation date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the indexes that were created on the specified date at or after the given time.
    
</dd>
</dl>

<dl>
<dd>

**updated_at:** `typing.Optional[str]` — Filter indexes by the last update date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the indexes that were last updated on the specified date at or after the given time.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.<a href="src/twelvelabs/indexes/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method creates an index.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.create(
    index_name="myIndex",
    models=[
        IndexesCreateRequestModelsItem(
            model_name="marengo3.0",
            model_options=["visual", "audio"],
        )
    ],
    addons=["thumbnail"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_name:** `str` — The name of the index. Make sure you use a succinct and descriptive name.
    
</dd>
</dl>

<dl>
<dd>

**models:** `typing.Sequence[IndexesCreateRequestModelsItem]` — An array that specifies the [video understanding models](/v1.3/docs/concepts/models) and the [model options](/v1.3/docs/concepts/modalities#model-options) to be enabled for this index. Models determine what tasks you can perform with your videos. Model options determine which modalities the platform analyzes.
    
</dd>
</dl>

<dl>
<dd>

**addons:** `typing.Optional[typing.Sequence[str]]` 

An array specifying which add-ons should be enabled. Each entry in the array is an addon, and the following values are supported:
- `thumbnail`: Enables thumbnail generation.

If you don't provide this parameter, no add-ons will be enabled.

<Note title="Notes">
- You can only enable addons when using the Marengo video understanding model.
- You cannot disable an add-on once the index has been created.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.<a href="src/twelvelabs/indexes/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves details about the specified index.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.retrieve(
    index_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — Unique identifier of the index to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.<a href="src/twelvelabs/indexes/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method updates the name of the specified index.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.update(
    index_id="6298d673f1090f1100476d4c",
    index_name="myIndex",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — Unique identifier of the index to update.
    
</dd>
</dl>

<dl>
<dd>

**index_name:** `str` — The name of the index.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.<a href="src/twelvelabs/indexes/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes the specified index and all the videos within it. This action cannot be undone.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.delete(
    index_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — Unique identifier of the index to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Assets
<details><summary><code>client.assets.<a href="src/twelvelabs/assets/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of assets in your account.

The platform returns your assets sorted by creation date, with the newest at the top of the list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.assets.list(
    page=1,
    page_limit=10,
    asset_ids=["6298d673f1090f1100476d4c", "6298d673f1090f1100476d4d"],
    asset_types=["image", "video", "document"],
    filename="meeting",
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**asset_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filters the response to include only assets with the specified identifiers. Provide one or more asset identifiers. When you specify multiple identifiers, the platform returns all matching assets.
    
</dd>
</dl>

<dl>
<dd>

**asset_types:** `typing.Optional[
    typing.Union[
        AssetsListRequestAssetTypesItem,
        typing.Sequence[AssetsListRequestAssetTypesItem],
    ]
]` — Filters the response to include only assets of the specified types. Provide one or more asset types. When you specify multiple types, the platform returns all matching assets.
    
</dd>
</dl>

<dl>
<dd>

**filename:** `typing.Optional[str]` — Filters the response to include only assets whose filename contains the specified string. The match is case-insensitive and supports partial matching.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.assets.<a href="src/twelvelabs/assets/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method creates an asset by uploading a file to the platform. Assets are reusable files that you can use in different workflows.

The platform processes uploads asynchronously. This method returns immediately with the asset in the `processing` status, which then transitions to the `ready` status on success or to the `failed` status when the file is invalid, corrupt, or unreadable. Poll the [Retrieve an asset](/v1.3/api-reference/upload-content/direct-uploads/retrieve) endpoint until the status of the asset is `ready` before you use it. This applies to every upload, including small files.

**Supported content**:
- Video, audio, and images.
- PDF, text, and Markdown files.

Filename extension matching is case-insensitive; for example, `notes.MD` and `notes.md` are treated the same. The platform rejects unsupported formats. For documents, it also rejects files whose extensions don't match the detected content.

**Upload methods**:
- **Local file**: Set the `method` parameter to `direct` and use the `file` parameter to specify the file.
- **Publicly accessible URL**: Set the `method` parameter to `url` and use the `url` parameter to specify the URL of your file.

**Upload limits**:
- **Video and audio, local files**: Up to 200 MB
- **Video and audio, public URLs**: Up to 4 GB
- **Images**: Up to 32 MB
- **Documents, local files**: Up to 200 MB
- **Documents, public URLs**: Up to 512 MB

Asset creation does not enforce a maximum duration for video and audio files. Each model applies its own file size and duration limits. For details, see the requirements below.

**Additional requirements** depend on your workflow:
- **Search**: [Marengo requirements](/v1.3/docs/concepts/models/marengo/marengo-3-0#video-file-requirements)
- **Video analysis**: [Pegasus requirements](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#input-requirements)
- **Entity search**: [Marengo image requirements](/v1.3/docs/concepts/models/marengo/marengo-3-0#image-file-requirements)
- **Create embeddings**: [Marengo requirements](/v1.3/docs/concepts/models/marengo/marengo-3-5#input-requirements)

<Note title="Note">
This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.assets.create(
    method="direct",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**method:** `AssetsCreateRequestMethod` — Specifies the upload method for the asset. Use `direct` to upload a local file or `url` for a publicly accessible URL.
    
</dd>
</dl>

<dl>
<dd>

**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**url:** `typing.Optional[str]` 

Specify this parameter to upload a file from a publicly accessible URL. This parameter is required when `method` is set to `url`.

Public video and audio URLs support up to 4 GB. Image URLs support up to 32 MB. Document URLs support up to 512 MB.

The parameter also accepts the URL of an HLS manifest (`.m3u8`) in VOD format. Live video streams are rejected with a `400` error. If the duration cannot be determined from the media, the platform calculates it from the manifest.
    
</dd>
</dl>

<dl>
<dd>

**filename:** `typing.Optional[str]` — The filename of the asset. If you provide a filename, the platform preserves it. If you omit it, the platform determines one from the file or URL.
    
</dd>
</dl>

<dl>
<dd>

**enable_hls:** `typing.Optional[bool]` 

The platform generates an HLS playlist and segments for streaming. Set to `false` to disable HLS generation. Applicable to video and audio assets only. The platform ignores this flag for other asset types.

**Default**: `true`.
    
</dd>
</dl>

<dl>
<dd>

**enable_thumbnail:** `typing.Optional[bool]` 

The platform generates thumbnail images from the uploaded content. Set to `false` to disable thumbnail generation.

For PDF files, the platform generates a representative thumbnail from the first page. Text and Markdown files do not produce thumbnails; the platform ignores this flag for them.

**Default**: `true`.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `typing.Optional[str]` — Metadata that helps you categorize your assets. You can specify a list of keys and values. Keys are strings, and values can be a string, a number, a boolean, or an array of strings. Send an integer wider than 53 bits (-9007199254740991 to 9007199254740991), and any identifier you want preserved verbatim, as a string. Send this value as a JSON-encoded string.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.assets.<a href="src/twelvelabs/assets/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves details about the specified asset.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.assets.retrieve(
    asset_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.assets.<a href="src/twelvelabs/assets/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes the specified asset. This action cannot be undone.

The delete fails with a `409 Conflict` error if other resources depend on the asset.

- **If knowledge store items use the asset**, in any status: the error code is `asset_has_knowledge_store_items`. The request fails even when you set the `force` query parameter to `true`. First delete the items with the [`DELETE`](/v1.3/api-reference/knowledge-store-items/delete) method of the `/knowledge-stores/{knowledge_store_id}/items/{item_id}` endpoint. Then delete the asset.
- **If indexed assets reference the asset**: the error code is `asset_has_linked_resources`. To delete the asset and these indexed assets together, set the `force` query parameter to `true`. To list the indexed assets first, use the [`GET`](/v1.3/api-reference/index-content/list-indexed-assets-by-asset) method of the `/assets/{asset_id}/indexed-assets` endpoint.
- **If both apply**: the error code is `asset_has_knowledge_store_items`.

**If entities use the asset**, a successful delete removes the asset from the `asset_ids` array of each entity. To list these entities, use the [`GET`](/v1.3/api-reference/entities/list-entities-by-asset) method of the `/assets/{asset_id}/entities` endpoint.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.assets.delete(
    asset_id="6298d673f1090f1100476d4c",
    force=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset to delete.
    
</dd>
</dl>

<dl>
<dd>

**force:** `typing.Optional[bool]` 

Use this parameter to choose how the delete handles indexed assets that reference the asset:

- `true`: Deletes the asset and the indexed assets that reference it.
- `false` or omitted: Fails with `409 Conflict` if indexed assets reference the asset.

If knowledge store items use the asset, the request fails with `409 Conflict` for either value. Delete the items first.

**Default**: `false`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.assets.<a href="src/twelvelabs/assets/client.py">retrieve_transcription</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves the transcription of a video or audio asset. An asset that has a transcription returns `200` with the current transcription status. The endpoint returns `404` when the asset cannot be found or has no transcription.

The platform generates transcriptions asynchronously. Poll this endpoint to monitor the transcription status.

When the status is `ready`, the response contains the segmentations you requested that the transcription supports. A transcription does not always support every segmentation, so read the segmentations the response returns rather than assuming every requested one is present.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.assets.retrieve_transcription(
    asset_id="6298d673f1090f1100476d4c",
    include=["words", "utterances"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset.
    
</dd>
</dl>

<dl>
<dd>

**include:** `typing.Optional[
    typing.Union[
        AssetsRetrieveTranscriptionRequestIncludeItem,
        typing.Sequence[AssetsRetrieveTranscriptionRequestIncludeItem],
    ]
]` 

Specifies the transcriptions to return. Each value segments the transcription differently:

- `words`: One entry for each word.
- `sentences`: One entry for each chunk the speech recognition model detects as a sentence.
- `utterances`: One entry for each speaker turn.

Send repeated values, such as the `?include=words&include=utterances` query string. The platform also accepts one comma-separated value, such as the `?include=words,utterances` query string.

**Default**: `words`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.assets.<a href="src/twelvelabs/assets/client.py">replace_user_metadata</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method replaces the entire user-defined metadata of the specified asset. Unlike the [`PATCH`](/v1.3/api-reference/upload-content/direct-uploads/update-user-metadata) method, which merges your changes with the existing metadata, this method overwrites the stored value in full:
- A key with a value creates or replaces that key.
- A key you omit, or set to an empty string (`""`), an empty array (`[]`), or `null`, is removed.

To clear all metadata, send an empty object (`{}`) in the `user_metadata` field. This produces the same result as the [`DELETE`](/v1.3/api-reference/upload-content/direct-uploads/delete-user-metadata) method.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.assets.replace_user_metadata(
    asset_id="6298d673f1090f1100476d4c",
    user_metadata={
        "category": "recentlyAdded",
        "batchNumber": 5,
        "rating": 9.3,
        "needsReview": True,
        "hashtags": ["summer", "vlog"],
    },
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset whose user-defined metadata to replace.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `UserMetadata` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.assets.<a href="src/twelvelabs/assets/client.py">delete_user_metadata</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes the user-defined metadata of the specified asset. To achieve the same result, you can also send an empty object (`{}`) in the `user_metadata` field of the [`PUT`](/v1.3/api-reference/upload-content/direct-uploads/replace-user-metadata) method.

This action cannot be undone.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.assets.delete_user_metadata(
    asset_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset whose user-defined metadata to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.assets.<a href="src/twelvelabs/assets/client.py">update_user_metadata</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method updates the user-defined metadata of the specified asset. The platform merges your changes with the existing metadata:
- A key with a value creates or replaces that key.
- A key set to `null` deletes that key.
- A key set to an empty string (`""`) or an empty array (`[]`) is ignored.
- A key you omit from the request keeps its current value.

To replace all metadata in a single call, use the [`PUT`](/v1.3/api-reference/upload-content/direct-uploads/replace-user-metadata) method of the `/assets/{asset_id}/user-metadata` endpoint instead.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.assets.update_user_metadata(
    asset_id="6298d673f1090f1100476d4c",
    user_metadata={
        "category": "recentlyAdded",
        "batchNumber": 5,
        "rating": 9.3,
        "needsReview": True,
        "hashtags": ["summer", "vlog"],
    },
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset whose user-defined metadata to update.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `UserMetadata` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.assets.<a href="src/twelvelabs/assets/client.py">enable_storage_accounting</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method enables storage accounting for the specified asset. Storage accounting makes an asset count toward your Managed Intelligence allowance.

**When to use this method**: Call it once for each asset that you uploaded before your plan moved to the new billing (a pre-migration asset). Enable storage accounting before you do either of the following:
- Add the asset to a knowledge store.
- Index the asset in an index for which Marengo is enabled.

An asset that you upload after your plan moves already counts toward your Managed Intelligence allowance. You do not need to call this method for it.

**Before you call this method**: The asset must have the `ready` status and a recorded size. To check, use the [`GET`](/v1.3/api-reference/manage-assets/retrieve) method of the `/assets/{asset_id}` endpoint and read the `status` and `size` fields.

**After you call this method**:
- The asset counts toward your Managed Intelligence allowance from the moment of the call.
- Enabling storage accounting is permanent. You cannot turn it off.
- If storage accounting is already on, the method returns the same response and changes nothing.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.assets.enable_storage_accounting(
    asset_id="6298d673f1090f1100476d4c",
    enabled=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset for which to enable storage accounting.
    
</dd>
</dl>

<dl>
<dd>

**enabled:** `bool` — Enables storage accounting for the asset. The only accepted value is `true`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## MultipartUpload
<details><summary><code>client.multipart_upload.<a href="src/twelvelabs/multipart_upload/client.py">list_incomplete_uploads</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of all incomplete multipart upload sessions in your account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.multipart_upload.list_incomplete_uploads(
    page=1,
    page_limit=10,
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.multipart_upload.<a href="src/twelvelabs/multipart_upload/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method creates a multipart upload session for a local file.

**Supported content**: Video, audio, and images.

**Upload limits**:
- **Video and audio**: Up to 10 GB
- **Images**: Up to 32 MB

**Additional requirements** depend on your workflow:
- **Search**: [Marengo requirements](/v1.3/docs/concepts/models/marengo/marengo-3-0#video-file-requirements)
- **Video analysis**: [Pegasus requirements](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#input-requirements)
- **Entity search**: [Marengo image requirements](/v1.3/docs/concepts/models/marengo/marengo-3-0#image-file-requirements)
- **Create embeddings**: [Marengo requirements](/v1.3/docs/concepts/models/marengo/marengo-3-5#input-requirements)
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.multipart_upload.create(
    filename="my-video.mp4",
    type="video",
    total_size=104857600,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**filename:** `str` — The original file name of the asset.
    
</dd>
</dl>

<dl>
<dd>

**type:** `CreateAssetUploadRequestType` — The type of asset you want to upload.
    
</dd>
</dl>

<dl>
<dd>

**total_size:** `int` 

The total size of the file in bytes. The platform uses this value to:
- Calculate the optimal chunk size.
- Determine the total number of chunks required
- Generate the initial set of presigned URLs

**Upload limits**:
- **Video and audio**: Up to 10 GB
- **Images**: Up to 32 MB
    
</dd>
</dl>

<dl>
<dd>

**enable_hls:** `typing.Optional[bool]` 

When set to `true`, the platform generates an HLS playlist and segments for streaming. Applicable to video and audio assets only. The platform ignores this flag for other asset types.

**Default**: `false`.
    
</dd>
</dl>

<dl>
<dd>

**enable_thumbnail:** `typing.Optional[bool]` 

When set to `true`, the platform generates thumbnail images from the uploaded content.

**Default**: `false`.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `typing.Optional[UserMetadata]` — Metadata that helps you categorize your assets. You can specify a list of keys and values. Keys are strings, and values can be a string, a number, a boolean, or an array of strings. A key set to an empty string (`""`), an empty array (`[]`), or `null` is omitted. Send an integer wider than 53 bits (-9007199254740991 to 9007199254740991), and any identifier you want preserved verbatim, as a string.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.multipart_upload.<a href="src/twelvelabs/multipart_upload/client.py">get_status</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method provides information about an upload session, including its current status, chunk-level progress, and completion state.

Use this method to:
- Verify upload completion (`status` = `completed`)
- Identify any failed chunks that require a retry
- Monitor the upload progress by comparing `uploaded_size` with `total_size`
- Determine if the session has expired
- Retrieve the status information for each chunk

After you report chunk completion, call this method to confirm the upload session reached the `completed` status. This status means the platform received the file, not that the asset is ready to use. The platform then validates the asset asynchronously. Poll the [Retrieve an asset](/v1.3/api-reference/upload-content/direct-uploads/retrieve) endpoint until the status of the asset is `ready` before you use it.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.multipart_upload.get_status(
    upload_id="507f1f77bcf86cd799439011",
    page=1,
    page_limit=10,
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**upload_id:** `str` — The unique identifier of the upload session.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.multipart_upload.<a href="src/twelvelabs/multipart_upload/client.py">report_chunk_batch</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method reports successfully uploaded chunks to the platform. The platform finalizes the upload after you report all chunks.


For optimal performance, report chunks in batches and in any order.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import CompletedChunk, TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.multipart_upload.report_chunk_batch(
    upload_id="507f1f77bcf86cd799439011",
    completed_chunks=[
        CompletedChunk(
            chunk_index=1,
            proof="d41d8cd98f00b204e9800998ecf8427e",
            proof_type="etag",
            chunk_size=5242880,
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**upload_id:** `str` — The unique identifier of the upload session.
    
</dd>
</dl>

<dl>
<dd>

**completed_chunks:** `typing.Sequence[CompletedChunk]` — The list of chunks successfully uploaded that you're reporting to the platform. Report only after receiving an ETag.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.multipart_upload.<a href="src/twelvelabs/multipart_upload/client.py">get_additional_presigned_urls</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method generates new presigned URLs for specific chunks that require uploading. Use this endpoint in the following situations:
- Your initial URLs have expired (URLs expire after one hour).
- The initial set of presigned URLs does not include URLs for all chunks.
- You need to retry failed chunk uploads with new URLs.
To specify which chunks need URLs, use the `start` and `count` parameters. For example, to generate URLs for chunks 21 to 30, use `start=21` and `count=10`.
The response will provide new URLs, each with a fresh expiration time of one hour.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.multipart_upload.get_additional_presigned_urls(
    upload_id="507f1f77bcf86cd799439011",
    start=1,
    count=10,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**upload_id:** `str` — The unique identifier of the upload session.
    
</dd>
</dl>

<dl>
<dd>

**start:** `int` — The index of the first chunk number to generate URLs for. Chunks are numbered from 1.
    
</dd>
</dl>

<dl>
<dd>

**count:** `int` — The number of presigned URLs to generate starting from the index. You can request a maximum of 50 URLs in a single API call.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EntityCollections
<details><summary><code>client.entity_collections.<a href="src/twelvelabs/entity_collections/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of the entity collections in your account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.entity_collections.list(
    page=1,
    page_limit=10,
    name="My entity collection",
    sort_by="created_at",
    sort_option="desc",
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — Filter entity collections by name.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[EntityCollectionsListRequestSortBy]` 

The field to sort on. The following options are available:
- `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the entity collection was updated.
- `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the entity collection was created.
- `name`: Sorts by the name.
    
</dd>
</dl>

<dl>
<dd>

**sort_option:** `typing.Optional[str]` 

The sorting direction. The following options are available:
- `asc`
- `desc`

**Default**: `desc`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.<a href="src/twelvelabs/entity_collections/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method creates an entity collection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.create(
    name="My entity collection",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the entity collection. Make sure you use a succinct and descriptive name.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — Optional description of the entity collection.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.<a href="src/twelvelabs/entity_collections/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves details about the specified entity collection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.retrieve(
    entity_collection_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.<a href="src/twelvelabs/entity_collections/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes the specified entity collection. This action cannot be undone.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.delete(
    entity_collection_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.<a href="src/twelvelabs/entity_collections/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method updates the specified entity collection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.update(
    entity_collection_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection to update.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The updated name of the entity collection.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — The updated description of the entity collection.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Knowledge stores
<details><summary><code>client.knowledge_stores.<a href="src/twelvelabs/knowledge_stores/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of the knowledge stores in your account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.knowledge_stores.list(
    page=1,
    page_limit=10,
    sort_by="created_at",
    sort_option="desc",
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[KnowledgeStoresListRequestSortBy]` 

The field to sort on. The following options are available:
- `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the knowledge store was created.
- `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the knowledge store was updated.

**Default**: `created_at`.
    
</dd>
</dl>

<dl>
<dd>

**sort_option:** `typing.Optional[str]` 

The sorting direction. The following options are available:
- `asc`
- `desc`

**Default**: `desc`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_stores.<a href="src/twelvelabs/knowledge_stores/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method creates a knowledge store.

Provide a name. Optionally include a description, a metadata map, and an `ingestion_config` object that controls how content added to the store is processed. The `ingestion_config` object is immutable after creation.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_stores.create(
    name="Product Demo Analysis",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**ingestion_config:** `typing.Optional[IngestionConfig]` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An optional description of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, KnowledgeStoreMetadataValue]]` — Custom metadata for the knowledge store, as user-defined key-value pairs. Up to 10 pairs, keys up to 128 characters, string values up to 2048 characters. Keys are strings; values can be a string, a number, a boolean, or an array of strings. A nested object, an array containing anything other than strings, and a null value are rejected. An integer must fit in 53 bits (-9007199254740991 to 9007199254740991). Send a wider integer, or an identifier that must be preserved verbatim, as a string.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_stores.<a href="src/twelvelabs/knowledge_stores/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves the details of a specific knowledge store.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_stores.retrieve(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_stores.<a href="src/twelvelabs/knowledge_stores/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes the specified knowledge store and all its items.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_stores.delete(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_stores.<a href="src/twelvelabs/knowledge_stores/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method updates the specified knowledge store. Only the `name`, `description`, and `metadata` fields can be updated.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_stores.update(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The name of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An optional description of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, KnowledgeStoreMetadataValue]]` — Custom metadata for the knowledge store, as user-defined key-value pairs. Up to 10 pairs, keys up to 128 characters, string values up to 2048 characters. Keys are strings; values can be a string, a number, a boolean, or an array of strings. A nested object, an array containing anything other than strings, and a null value are rejected. An integer must fit in 53 bits (-9007199254740991 to 9007199254740991). Send a wider integer, or an identifier that must be preserved verbatim, as a string. The provided object replaces the existing metadata in full, so include every key you want to keep and omit the ones you want to remove. To clear all metadata, set this field to an empty object (`{}`).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_stores.<a href="src/twelvelabs/knowledge_stores/client.py">search</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method searches a knowledge store using natural language and returns matching video clips and images ranked by relevance.

Use the `query.text` field to specify your natural-language query. Use the `filter` parameter to choose which items to search. Use the `search_options` parameter to choose how the platform matches videos.

By default, each result is an individual match: a video clip or an image. Set the `group_by` parameter to `item` to group clips under their parent item.

<Note title="Note">
This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import (
    KnowledgeStoreSearchQuery,
    SearchKnowledgeStoreOptions,
    TwelveLabs,
    VideoSearchOptions,
)

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_stores.search(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    query=KnowledgeStoreSearchQuery(
        text="A person cooking pasta",
    ),
    search_options=SearchKnowledgeStoreOptions(
        video=VideoSearchOptions(
            modalities=["visual", "audio"],
        ),
    ),
    group_by="none",
    page_size=10,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**query:** `KnowledgeStoreSearchQuery` 
    
</dd>
</dl>

<dl>
<dd>

**filter:** `typing.Optional[SearchKnowledgeStoreFilter]` 
    
</dd>
</dl>

<dl>
<dd>

**search_options:** `typing.Optional[SearchKnowledgeStoreOptions]` 
    
</dd>
</dl>

<dl>
<dd>

**group_by:** `typing.Optional[SearchKnowledgeStoreRequestGroupBy]` 

Controls how the platform groups matches in the response.

- `none`: Returns individual matches ordered by relevance.
- `item`: Groups matches under their parent item.

**Default**: `none`.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

The maximum number of results per page. A result is one entry in the `data` array. With the `group_by` parameter set to its default of `none`, each result is an individual match: a video clip or an image. When set to `item`, each result is one item: a video with all its matching clips, or an image.

**Default**: `10`. **Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**page_token:** `typing.Optional[str]` 

Pagination token used to retrieve the next page of results. Omit it on the first request. To fetch the next page, set it to the `next_page_token` field returned in the previous response and send the request again.

If a token is malformed or unrecognized, the platform returns a `400` error. If a token has expired, the platform returns a `410` error (make a new search request to obtain a fresh page token).
    
</dd>
</dl>

<dl>
<dd>

**include_metadata:** `typing.Optional[bool]` 

Set to `true` to include metadata in each result. Each result includes a `metadata` object with these fields:

- `system`: System-generated metadata, such as duration and resolution.
- `user`: The custom metadata of the source asset.
- `item`: The custom metadata of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Knowledge store items
<details><summary><code>client.knowledge_store_items.<a href="src/twelvelabs/knowledge_store_items/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of items in the specified knowledge store.

Use the `status`, `metadata`, `enrichment`, `created_at_gte`, and `created_at_lte` parameters to choose which items to list. An item must match all of the parameters that you specify.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
import datetime

from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.knowledge_store_items.list(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    page=1,
    page_limit=10,
    sort_by="created_at",
    sort_option="desc",
    status=["queued"],
    metadata='{"hashtags":["summer","travel"],"verified":true}',
    enrichment='{"detected_topic":"cooking"}',
    created_at_gte=datetime.datetime.fromisoformat(
        "2026-09-01 00:00:00+00:00",
    ),
    created_at_lte=datetime.datetime.fromisoformat(
        "2026-09-30 23:59:59+00:00",
    ),
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[KnowledgeStoreItemsListRequestSortBy]` 

The field to sort on. The following options are available:
- `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was created.
- `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was last updated.

**Default**: `created_at`.
    
</dd>
</dl>

<dl>
<dd>

**sort_option:** `typing.Optional[str]` 

The sorting direction. The following options are available:
- `asc`
- `desc`

**Default**: `desc`.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[
    typing.Union[
        KnowledgeStoreItemsListRequestStatusItem,
        typing.Sequence[KnowledgeStoreItemsListRequestStatusItem],
    ]
]` 

Filter by one or more item processing statuses. For the meaning of each value, see the
[Item statuses](/v1.3/api-reference/knowledge-store-items/the-knowledge-store-item-object#item-statuses)
section on **The knowledge store item object** page.

To filter by multiple statuses, repeat the `status` parameter for each value:
```
status=queued&status=pending
```
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[str]` 

Filter by custom metadata. Provide a JSON object that maps each key to a value or to a list of values. A list matches any of its values. An item must match all of the keys that you specify.

A key matches the custom metadata of the source asset (the `metadata` field of the knowledge store item) and the custom metadata of the knowledge store item (the `item_metadata` field). An item matches a key when the value matches in either field.

A value is a string, a number, or a boolean. The value must have the same type as the value that the item has for the key. For example, the number `2026` does not match the string `"2026"`. If the item has a list for the key, the item matches when the list contains the value.

The object must have at least one key. A list must have at least one value. If the parameter is not a valid JSON object, or a value is not a string, a number, or a boolean, the platform returns a `422` error.

URL-encode the object:
```
metadata=%7B%22hashtags%22%3A%5B%22summer%22%2C%22travel%22%5D%2C%22verified%22%3Atrue%7D
```
    
</dd>
</dl>

<dl>
<dd>

**enrichment:** `typing.Optional[str]` 

Filter by enrichment values. The platform extracts these values as the enrichment configuration of the knowledge store defines (the `ingestion_config.enrichment_config` field).

Provide a JSON object that maps each top-level property that the enrichment configuration defines to a value or to a list of values. Each value follows the rules for the `metadata` parameter. If you specify a key that the enrichment configuration does not define, the platform returns a `422` error.

The `granularity` keyword of a property sets how often the platform extracts its value. The keyword also sets which items the key matches:

- `video`: One value for each video. The key matches video items only.
- `image`: One value for each image. The key matches image items only.
- `shot`: One value for each shot of a video. A shot is a continuous part of a video between two scene changes. The key matches video items only. If you specify more than one `shot` key, one shot must have all of the values.

An item must match all of the keys that you specify. An object with a `video` key and an `image` key matches no items, because an item is a video or an image.

URL-encode the object:
```
enrichment=%7B%22detected_topic%22%3A%22cooking%22%7D
```
    
</dd>
</dl>

<dl>
<dd>

**created_at_gte:** `typing.Optional[dt.datetime]` 

Return only items created at or after this time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ").

The creation time is the time when you create the item with the [`POST`](/v1.3/api-reference/knowledge-store-items/create) method of the `/knowledge-stores/{knowledge_store_id}/items` endpoint. It is not the time when the item reaches the `ready` status. To list only items that are ready, also set the `status` parameter to `ready`.
    
</dd>
</dl>

<dl>
<dd>

**created_at_lte:** `typing.Optional[dt.datetime]` 

Return only items created at or before this time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). When you use both `created_at_gte` and `created_at_lte`, the `created_at_gte` time must be equal to or earlier than the `created_at_lte` time. Otherwise, the platform returns a `422` error.

The creation time is the time when you create the item with the [`POST`](/v1.3/api-reference/knowledge-store-items/create) method of the `/knowledge-stores/{knowledge_store_id}/items` endpoint. It is not the time when the item reaches the `ready` status.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_items.<a href="src/twelvelabs/knowledge_store_items/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method adds an asset to a knowledge store for processing.
The operation is asynchronous. The item is created immediately with the `queued`
status and processed in the background.

**Asset size limits**:
- **Video**: Up to 10 GB
- **Images**: Up to 32 MB
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_items.create(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    asset_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset to add to the knowledge store. If you uploaded the asset before your plan moved to the new billing, enable storage accounting for it before you add it to a knowledge store. Use the [Enable storage accounting for an asset](/v1.3/api-reference/manage-assets/enable-storage-accounting) method.
    
</dd>
</dl>

<dl>
<dd>

**asset_type:** `typing.Optional[KnowledgeStoreItemAssetType]` — The type of item to create.
    
</dd>
</dl>

<dl>
<dd>

**item_metadata:** `typing.Optional[typing.Dict[str, KnowledgeStoreMetadataValue]]` — Custom metadata for the item, as user-defined key-value pairs. Up to 50 pairs, keys up to 128 characters, string values up to 8192 characters. Keys are strings; values can be a string, a number, a boolean, or an array of strings. A nested object, an array containing anything other than strings, and a null value are rejected. An integer must fit in 53 bits (-9007199254740991 to 9007199254740991). Send a wider integer, or an identifier that must be preserved verbatim, as a string. To change it after you create the item, use the [`PATCH`](/v1.3/api-reference/knowledge-store-items/update-item-metadata) or [`PUT`](/v1.3/api-reference/knowledge-store-items/replace-item-metadata) method of the `/knowledge-stores/{knowledge_store_id}/items/{item_id}/item-metadata` endpoint.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, KnowledgeStoreMetadataValue]]` — Deprecated. Use `item_metadata` instead. The item stores the pairs in its `item_metadata` field and not in its `metadata` field. Send `item_metadata` or `metadata`, not both. A request that sets both returns a `400` error.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_items.<a href="src/twelvelabs/knowledge_store_items/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves the details of a specific knowledge store item.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_items.retrieve(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    item_id="ksi_069e9870-3c4d-7abc-9012-3456789abcde",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` — The unique identifier of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_items.<a href="src/twelvelabs/knowledge_store_items/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes the specified knowledge store item.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_items.delete(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    item_id="ksi_069e9870-3c4d-7abc-9012-3456789abcde",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` — The unique identifier of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_items.<a href="src/twelvelabs/knowledge_store_items/client.py">replace_knowledge_store_item_metadata</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method replaces the entire `item_metadata` of the specified knowledge store item and returns the item. Unlike the [`PATCH`](/v1.3/api-reference/knowledge-store-items/update-item-metadata) method, which merges your changes with the existing metadata, this method overwrites the stored value in full:
- A key with a value creates or replaces that key.
- A key you omit, or set to an empty string (`""`), an empty array (`[]`), or `null`, is removed.

To clear all item metadata, send an empty object (`{}`) in the `item_metadata` field. The `metadata` field of the item does not change.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_items.replace_knowledge_store_item_metadata(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    item_id="ksi_069e9870-3c4d-7abc-9012-3456789abcde",
    item_metadata={"creator_handle": "@jane.doe", "view_count": 48210},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` — The unique identifier of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**item_metadata:** `typing.Dict[str, typing.Optional[KnowledgeStoreMetadataEditValue]]` — The complete `item_metadata` of the item after the request. Up to 50 pairs. Keys are strings of up to 128 characters. String values can have up to 8192 characters. Values can be a string, a number, a boolean, or an array of strings. A nested object and an array containing anything other than strings are rejected. An integer must fit in 53 bits (-9007199254740991 to 9007199254740991). Send a wider integer, or an identifier that must be preserved verbatim, as a string.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_items.<a href="src/twelvelabs/knowledge_store_items/client.py">update_knowledge_store_item_metadata</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method updates the `item_metadata` of the specified knowledge store item and returns the item. The platform merges your changes with the existing metadata:
- A key with a value creates or replaces that key.
- A key set to `null` deletes that key.
- A key set to an empty string (`""`) or an empty array (`[]`) is ignored.
- A key you omit from the request keeps its current value.

The `metadata` field of the item does not change. If the merged result contains more than 50 pairs, the request fails.

To replace all item metadata in a single call, use the [`PUT`](/v1.3/api-reference/knowledge-store-items/replace-item-metadata) method of the `/knowledge-stores/{knowledge_store_id}/items/{item_id}/item-metadata` endpoint instead.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_items.update_knowledge_store_item_metadata(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    item_id="ksi_069e9870-3c4d-7abc-9012-3456789abcde",
    item_metadata={"creator_handle": "@jane.doe", "view_count": 48210},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` — The unique identifier of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**item_metadata:** `typing.Dict[str, typing.Optional[KnowledgeStoreMetadataEditValue]]` — The keys to change. Send at least one key. Keys are strings of up to 128 characters. String values can have up to 8192 characters. Values can be a string, a number, a boolean, an array of strings, or `null` to delete the key. A nested object and an array containing anything other than strings are rejected. An integer must fit in 53 bits (-9007199254740991 to 9007199254740991). Send a wider integer, or an identifier that must be preserved verbatim, as a string.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Knowledge store item tags
<details><summary><code>client.knowledge_store_item_tags.<a href="src/twelvelabs/knowledge_store_item_tags/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns the tags of the specified knowledge store item. The platform sorts the tags by `start_sec`, earliest first. Tags with the same `start_sec` are sorted by `_id`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.knowledge_store_item_tags.list(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    item_id="ksi_069e9870-3c4d-7abc-9012-3456789abcde",
    page=1,
    page_limit=10,
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` — The unique identifier of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_tags.<a href="src/twelvelabs/knowledge_store_item_tags/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method tags a moment or a range of a video item and returns the tag. Set `start_sec` to tag a moment. Set `start_sec` and `end_sec` to tag a range. A video item holds up to 100 tags. The method returns a 422 error for an item that is not a video item, and when the item already holds 100 tags.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_tags.create(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    item_id="ksi_069e9870-3c4d-7abc-9012-3456789abcde",
    start_sec=12.5,
    end_sec=18.25,
    tag_metadata={"event": "goal", "team": "home"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` — The unique identifier of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**start_sec:** `float` — The start of the tag, in seconds from the start of the video. It must be less than the duration of the video.
    
</dd>
</dl>

<dl>
<dd>

**tag_metadata:** `typing.Dict[str, KnowledgeStoreMetadataValue]` — The custom metadata of the tag, as key-value pairs. Send at least one key. Up to 50 pairs. Keys are strings of up to 128 characters. String values can have up to 8192 characters. Values can be a string, a number, a boolean, or an array of strings. A nested object, an array containing anything other than strings, and a null value are rejected. An integer must fit in 53 bits (-9007199254740991 to 9007199254740991). Send a wider integer, or an identifier that must be preserved verbatim, as a string.
    
</dd>
</dl>

<dl>
<dd>

**end_sec:** `typing.Optional[float]` — The end of the range, in seconds from the start of the video. It must be greater than `start_sec`. It must not exceed the duration of the video. Omit it, or send `null`, to tag a single moment.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_tags.<a href="src/twelvelabs/knowledge_store_item_tags/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves the details of a specific tag of a knowledge store item.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_tags.retrieve(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    item_id="ksi_069e9870-3c4d-7abc-9012-3456789abcde",
    tag_id="ksit_069e9870-3c4d-7abc-9012-3456789abcde",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` — The unique identifier of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**tag_id:** `str` — The unique identifier of the item tag.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_tags.<a href="src/twelvelabs/knowledge_store_item_tags/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes the specified tag of a knowledge store item.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_tags.delete(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    item_id="ksi_069e9870-3c4d-7abc-9012-3456789abcde",
    tag_id="ksit_069e9870-3c4d-7abc-9012-3456789abcde",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` — The unique identifier of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**tag_id:** `str` — The unique identifier of the item tag.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_tags.<a href="src/twelvelabs/knowledge_store_item_tags/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method updates the range or the `tag_metadata` of the specified tag and returns the tag. Send at least one field. A field you omit keeps its current value. To clear the end of the range, send `end_sec` as `null`. The tag becomes a single moment. The platform merges your changes to `tag_metadata` with the existing metadata:
- A key with a value creates or replaces that key.
- A key set to `null` deletes that key.
- A key set to an empty string (`""`) or an empty array (`[]`) is ignored.
- A key you omit from the request keeps its current value.

The tag must keep at least one key in `tag_metadata`, and it holds up to 50 pairs. If the merged result breaks either limit, the request fails.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_tags.update(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    item_id="ksi_069e9870-3c4d-7abc-9012-3456789abcde",
    tag_id="ksit_069e9870-3c4d-7abc-9012-3456789abcde",
    end_sec=18.25,
    tag_metadata={},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**item_id:** `str` — The unique identifier of the knowledge store item.
    
</dd>
</dl>

<dl>
<dd>

**tag_id:** `str` — The unique identifier of the item tag.
    
</dd>
</dl>

<dl>
<dd>

**start_sec:** `typing.Optional[float]` — The new start of the tag, in seconds from the start of the video. It must be less than the duration of the video. The tag must still end after it starts.
    
</dd>
</dl>

<dl>
<dd>

**end_sec:** `typing.Optional[float]` — The new end of the range, in seconds from the start of the video. It must be greater than `start_sec`. It must not exceed the duration of the video. Send `null` to clear the end, which turns a range into a single moment. Omit the field to keep the current end.
    
</dd>
</dl>

<dl>
<dd>

**tag_metadata:** `typing.Optional[
    typing.Dict[str, typing.Optional[KnowledgeStoreMetadataEditValue]]
]` — The keys to change. Send at least one key. Keys are strings of up to 128 characters. String values can have up to 8192 characters. Values can be a string, a number, a boolean, an array of strings, or `null` to delete the key. A key you omit keeps its current value. A nested object and an array containing anything other than strings are rejected. The tag holds up to 50 pairs after the merge. An integer must fit in 53 bits (-9007199254740991 to 9007199254740991). Send a wider integer, or an identifier that must be preserved verbatim, as a string.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Knowledge store item collections
<details><summary><code>client.knowledge_store_item_collections.<a href="src/twelvelabs/knowledge_store_item_collections/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of the item collections in the specified knowledge store.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.knowledge_store_item_collections.list(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    page=1,
    page_limit=10,
    sort_by="created_at",
    sort_option="desc",
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[KnowledgeStoreItemCollectionsListRequestSortBy]` 

The field to sort on. The following options are available:
- `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item collection was created.
- `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item collection was last updated.
- `name`: Sorts alphabetically by the name of the item collection.

**Default**: `created_at`.
    
</dd>
</dl>

<dl>
<dd>

**sort_option:** `typing.Optional[str]` 

The sorting direction. The following options are available:
- `asc`
- `desc`

**Default**: `desc`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_collections.<a href="src/twelvelabs/knowledge_store_item_collections/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates an item collection in the specified knowledge store. An item collection is a named collection of items. Use item collections to organize and reference subsets of items together.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_collections.create(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    name="Q1 highlights",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the item collection. Must be unique within the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An optional description of the item collection.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, KnowledgeStoreMetadataValue]]` — Custom metadata for the item collection, as user-defined key-value pairs. Up to 10 pairs, keys up to 128 characters, string values up to 2048 characters. Keys are strings; values can be a string, a number, a boolean, or an array of strings. A nested object, an array containing anything other than strings, and a null value are rejected. An integer must fit in 53 bits (-9007199254740991 to 9007199254740991). Send a wider integer, or an identifier that must be preserved verbatim, as a string.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_collections.<a href="src/twelvelabs/knowledge_store_item_collections/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves the details of a specific item collection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_collections.retrieve(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    collection_id="ksic_069e9870-3c4d-7abc-9012-3456789abcde",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**collection_id:** `str` — The unique identifier of the knowledge store item collection.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_collections.<a href="src/twelvelabs/knowledge_store_item_collections/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes the specified item collection. The items themselves remain in the knowledge store.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_collections.delete(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    collection_id="ksic_069e9870-3c4d-7abc-9012-3456789abcde",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**collection_id:** `str` — The unique identifier of the knowledge store item collection.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_collections.<a href="src/twelvelabs/knowledge_store_item_collections/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the `name`, `description`, and `metadata` fields of the specified item collection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_collections.update(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    collection_id="ksic_069e9870-3c4d-7abc-9012-3456789abcde",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**collection_id:** `str` — The unique identifier of the knowledge store item collection.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The name of the item collection. Must be unique within the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An optional description of the item collection.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, KnowledgeStoreMetadataValue]]` — Custom metadata for the item collection, as user-defined key-value pairs. Up to 10 pairs, keys up to 128 characters, string values up to 2048 characters. Keys are strings; values can be a string, a number, a boolean, or an array of strings. A nested object, an array containing anything other than strings, and a null value are rejected. An integer must fit in 53 bits (-9007199254740991 to 9007199254740991). Send a wider integer, or an identifier that must be preserved verbatim, as a string. The provided object replaces the existing metadata in full, so include every key you want to keep and omit the ones you want to remove. To clear all metadata, set this field to an empty object (`{}`).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_collections.<a href="src/twelvelabs/knowledge_store_item_collections/client.py">list_items</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of the items in the specified item collection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.knowledge_store_item_collections.list_items(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    collection_id="ksic_069e9870-3c4d-7abc-9012-3456789abcde",
    page=1,
    page_limit=10,
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**collection_id:** `str` — The unique identifier of the knowledge store item collection.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_collections.<a href="src/twelvelabs/knowledge_store_item_collections/client.py">add_items</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Adds one or more items to the specified item collection. This operation is idempotent — items already in the collection are skipped. Every identifier must reference an existing item in the knowledge store.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_collections.add_items(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    collection_id="ksic_069e9870-3c4d-7abc-9012-3456789abcde",
    item_ids=["ksi_069e9870-3c4d-7abc-9012-3456789abcde"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**collection_id:** `str` — The unique identifier of the knowledge store item collection.
    
</dd>
</dl>

<dl>
<dd>

**item_ids:** `typing.Sequence[str]` — The unique identifiers of the items to add to the collection. Include up to 500 identifiers per request.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.knowledge_store_item_collections.<a href="src/twelvelabs/knowledge_store_item_collections/client.py">remove_items</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Removes one or more items from the specified item collection. This operation is idempotent — identifiers that do not match a member of the collection are ignored. The items themselves remain in the knowledge store.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.knowledge_store_item_collections.remove_items(
    knowledge_store_id="ks_069e9869-1ea3-7481-8000-dae72bf6be6e",
    collection_id="ksic_069e9870-3c4d-7abc-9012-3456789abcde",
    item_ids=["ksi_069e9870-3c4d-7abc-9012-3456789abcde"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store.
    
</dd>
</dl>

<dl>
<dd>

**collection_id:** `str` — The unique identifier of the knowledge store item collection.
    
</dd>
</dl>

<dl>
<dd>

**item_ids:** `typing.Sequence[str]` — The unique identifiers of the items to remove from the collection. Include up to 500 identifiers per request.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Embed
<details><summary><code>client.embed.<a href="src/twelvelabs/embed/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Note title="Note">
  This endpoint will be deprecated in a future version. Migrate to the [Embed API v2](/v1.3/api-reference/create-embeddings-v2) for continued support and access to new features.
</Note>

This method creates embeddings for text, image, and audio content.

Ensure your media files meet the following requirements:
- [Audio files](/v1.3/docs/concepts/models/marengo/marengo-3-0#audio-file-requirements).
- [Images](/v1.3/docs/concepts/models/marengo/marengo-3-0#image-file-requirements).

Parameters for embeddings:
- **Common parameters**:
  - `model_name`: The video understanding model you want to use. Example: "marengo3.0".
- **Text embeddings**:
  - `text`: Text for which to create an embedding.
- **Image embeddings**:
  Provide one of the following:
  - `image_url`: Publicly accessible URL of your image file.
  - `image_file`:  Local image file.
- **Audio embeddings**:
  Provide one of the following:
  - `audio_url`: Publicly accessible URL of your audio file.
  - `audio_file`: Local audio file.

<Note title="Notes">
- The Marengo video understanding model generates embeddings for all modalities in the same latent space. This shared space enables any-to-any searches across different types of content.
- You can create multiple types of embeddings in a single API call.
- Audio embeddings combine generic sound and human speech in a single embedding. For videos with transcriptions, you can retrieve transcriptions and then [create text embeddings](/v1.3/api-reference/create-embeddings-v1/text-image-audio-embeddings/create-text-image-audio-embeddings) from these
- This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page. When a request exceeds the limit for one type of content, the platform can return `200` instead of `429`. The result for that type then contains the rate limit message in `error_message` and no embedding.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.create(
    model_name="model_name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_name:** `str` 

The name of the model you want to use. The following models are available:
  - `marengo3.0`: Enhanced model with sports intelligence and extended content support.
    
</dd>
</dl>

<dl>
<dd>

**text:** `typing.Optional[str]` 

The text for which you wish to create an embedding.

**Example**: "Man with a dog crossing the street"
    
</dd>
</dl>

<dl>
<dd>

**image_url:** `typing.Optional[str]` — The publicly accessible URL of the image for which you wish to create an embedding. This parameter is required for image embeddings if `image_file` is not provided.
    
</dd>
</dl>

<dl>
<dd>

**image_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**audio_url:** `typing.Optional[str]` — The publicly accessible URL of the audio file for which you wish to creae an embedding. This parameter is required for audio embeddings if `audio_file` is not provided.
    
</dd>
</dl>

<dl>
<dd>

**audio_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**audio_start_offset_sec:** `typing.Optional[float]` 

Specifies the start time, in seconds, from which the platform generates the audio embeddings. This parameter allows you to skip the initial portion of the audio during processing.
**Default**: `0`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Search
<details><summary><code>client.search.<a href="src/twelvelabs/search/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this endpoint to search for relevant matches in an index using text, media, or a combination of both as your query.

**Text queries**:
- Use the `query_text` parameter to specify your query.

**Media queries**:
- Set the `query_media_type` parameter to the corresponding media type (example: `image`).
- Provide up to 10 images by specifying the following parameters multiple times:
  - `query_media_url`: Publicly accessible URL of your media file.
  - `query_media_file`: Local media file.
**Composed text and media queries**:
- Use the `query_text` parameter for your text query.
- Set `query_media_type` to `image`.
- Provide up to 10 images by specifying the `query_media_url` and `query_media_file` parameters multiple times.

**Entity search** (beta):
- To find a specific person in your videos, enclose the unique identifier of the entity you want to find in the `query_text` parameter.

<Note title="Notes">
- When using images in your search queries (either as media queries or in composed searches), ensure your images meet the [requirements](/v1.3/docs/concepts/models/marengo/marengo-3-0#image-file-requirements).
- This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.search.create(
    index_id="index_id",
    search_options=["visual"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index to search.
    
</dd>
</dl>

<dl>
<dd>

**search_options:** `typing.List[SearchCreateRequestSearchOptionsItem]` 

Specifies the modalities the video understanding model uses to find relevant information.

Available options:
- `visual`: Searches visual content.
- `audio`: Searches non-speech audio.
- `transcription`: Spoken words

<Note title="Note">
- You can specify multiple search options in conjunction with the [`operator`](/v1.3/api-reference/any-to-video-search/make-search-request#request.body.operator.operator) parameter described below to broaden or narrow your search. For example, to search using both visual and non-speech audio content, include this parameter two times in the request as shown below:
  ```JSON
  --form search_options=visual \
  --form search_options=audio \
  --form search_options=transcription \
  ```
</Note>

For guidance, see the [Search options](/v1.3/docs/concepts/modalities#search-options) section.
    
</dd>
</dl>

<dl>
<dd>

**query_media_type:** `typing.Optional[SearchCreateRequestQueryMediaType]` — The type of media you wish to use. This parameter is required for media queries. For example, to perform an image-based search, set this parameter to `image`. Use `query_text` together with this parameter when you want to perform a composed image+text search.
    
</dd>
</dl>

<dl>
<dd>

**query_media_url:** `typing.Optional[str]` 

The publicly accessible URL of a media file to use as a query. This parameter is required for media queries if `query_media_file` is not provided.

You can provide up to 10 images by specifying this parameter multiple times (Marengo 3.0 only):
```
--form query_media_url=https://example.com/image1.jpg \
--form query_media_url=https://example.com/image2.jpg
```
    
</dd>
</dl>

<dl>
<dd>

**query_media_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**query_text:** `typing.Optional[str]` 

The text query to search for. This parameter is required for text queries. Note that the platform supports full natural language-based search. You can use this parameter together with `query_media_type` and `query_media_url` or `query_media_file` to perform a composed image+text search.

If you're using the Entity Search feature to search for specific persons in your video content, you must enclose the unique identifier of your entity between the `<@` and `>` markers. For example, to search for an entity with the ID `entity123`, use `<@entity123> is walking` as your query.


Marengo supports up to 500 tokens per query.
    
</dd>
</dl>

<dl>
<dd>

**transcription_options:** `typing.Optional[typing.List[SearchCreateRequestTranscriptionOptionsItem]]` 

Specifies how the platform matches your text query with the words spoken in the video. This parameter applies only when the `search_options` parameter contains the `transcription` value.

Available options:
- `lexical`: Exact word matching
- `semantic`: Meaning-based matching

For details on when to use each option, see the [Transcription options](/v1.3/docs/concepts/modalities#transcription-options) section.

**Default**: `["lexical", "semantic"]`.
    
</dd>
</dl>

<dl>
<dd>

**group_by:** `typing.Optional[SearchCreateRequestGroupBy]` 

Use this parameter to group or ungroup items in a response. It can take one of the following values:
- `video`:  The platform will group the matching video clips in the response by video.
- `clip`: The matching video clips in the response will not be grouped.

**Default:** `clip`
    
</dd>
</dl>

<dl>
<dd>

**operator:** `typing.Optional[SearchCreateRequestOperator]` 

Combines multiple search options using `or` or `and`. Use `and` to find segments matching all search options. Use `or` to find segments matching any search option. For detailed guidance on using this parameter, see the [Combine multiple modalities](/v1.3/docs/concepts/modalities#combine-multiple-modalities) section.

**Default**: `or`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page. When grouping by video, this parameter represents the number of videos per page. Otherwise, it represents the maximum number of video clips per page.

**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**filter:** `typing.Optional[str]` 

Specifies a stringified JSON object to filter your search results. Supports both system-generated metadata (example: video ID, duration) and user-defined metadata.

**Syntax for filtering**

The following table describes the supported data types, operators, and filter syntax:

| Data type | Operator | Description | Syntax |
|:----------|:---------|:------------|:-------|
| String | `=` | Matches results equal to the specified value. | `{"field": "value"}`
| Array of strings | `=` | Matches results with any value in the specified array. Supported only for `id`. | `{"id": ["value1", "value2"]}` |
| Numeric (integer, float) | `=`, `lte`, `gte` | Matches results equal to or within a range of the specified value. | `{"field": number}` or `{"field": { "gte": number, "lte": number }}` |
| Boolean | `=` | Matches results equal to the specified boolean value. | `{"field": true}` or `{"field": false}`. |

<br/>
**System-generated metadata**

The table below describes the system-generated metadata available for filtering your  search results:

| Field name | Description | Type | Example |
|:-----------|:------------|:-----|:--------|
| `id` | Filters by specific video IDs. | Array of strings | `{"id": ["67cec9caf45d9b64a58340fc", "67cec9baf45d9b64a58340fa"]}`. |
| `duration` | Filters based on the duration of the video containing the segment that matches your query. | Number or object with `gte` and `lte` | `{"duration": 600}` or `{"duration": { "gte": 600, "lte": 800 }}` |
| `width` | Filters by video width (in pixels). | Number or object with `gte` and `lte` | `{"width": 1920}` or `{"width": { "gte": 1280, "lte": 1920}}` |
| `height` | Filters by video height (in pixels). | Number or object with `gte` and `lte`. | `{"height": 1080}` or `{"height": { "gte": 720, "lte": 1080 }}`. |
| `size` | Filters by video size (in bytes) | Number or object with `gte` and `lte`. | `{"size": 1048576}` or `{"size": { "gte": 1048576, "lte": 5242880}}` |
| `filename` | Filters by the exact file name. | String | `{"filename": "Animal Encounters part 1"}` |

<br/>
**User-defined metadata**

To filter by user-defined metadata:
1. Add metadata to your video by calling the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/:index-id/videos/:video-id` endpoint
2. Reference the custom field in your filter object. For example, to filter videos where a custom field named `needsReview` of type boolean is `true`, use `{"needs_review": true}`.

For more details and examples, see the [Filter search results](/v1.3/docs/guides/search/filtering) page.
    
</dd>
</dl>

<dl>
<dd>

**include_user_metadata:** `typing.Optional[bool]` — Specifies whether to include user-defined metadata in the search results.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.search.<a href="src/twelvelabs/search/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this endpoint to retrieve a specific page of search results.

<Note title="Note">
When you use pagination, you will not be charged for retrieving subsequent pages of results.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.search.retrieve(
    page_token="1234567890",
    include_user_metadata=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page_token:** `str` — A token that identifies the page to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**include_user_metadata:** `typing.Optional[bool]` — Specifies whether to include user-defined metadata in the search results.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Responses
<details><summary><code>client.responses.<a href="src/twelvelabs/responses/client.py">create_stream</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method uses [Jockey](/v1.3/agents/concepts/jockey) to reason over content in a knowledge store and create a response. It uses [Open Responses](https://www.openresponses.org/specification) conventions for input items and streaming events.

Before you use this method, you must create an asset, create a knowledge store, and add the asset to the knowledge store as an item.

**Multi-turn conversations**: Supported via a session identifier. The first request implicitly creates a session; subsequent requests pass the returned identifier to continue the conversation.

**Selections**: By default, Jockey reasons over every item in the knowledge store. To narrow the scope, set the optional `selections` parameter to specific items or item collections, then reference each one with a `{{sel:N}}` token in the `content` field of an `input` item (`N` is the zero-based position in the `selections` array). The narrowing is applied at the prompt level; the knowledge store does not block access to other items.

**Streaming**: Set the `stream` parameter to `true` to receive the response as [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) (SSE). The reply streams in as a sequence of typed events and ends with a `data: [DONE]` message.

**Web sources**: Jockey can search public web sources while it generates a response. To allow this, include `{ "type": "jockey:web_search" }` in the `tools` array. The response can then cite these sources alongside content from the knowledge store, as `url_citation` annotations. Jockey decides whether to use an available tool, so enabling web search does not guarantee a search. To make a search more likely, explicitly tell Jockey what information to look up in `input` or `instructions`. A prompt that asks Jockey to search the web does not enable web search by itself. If you omit `tools` or pass `[]`, Jockey cannot search public web sources, even when the prompt requests it.

<Accordion title="Example response">
```json
{
  "id": "resp_019f4f2a-b69e-7812-b20f-6ea6d644ceff",
  "type": "response",
  "object": "response",
  "status": "completed",
  "incomplete_details": null,
  "session_id": "sess_019f4f2a-b69b-7a01-9018-cc51681121ea",
  "knowledge_store_id": "ks_019ebcf4-7e08-7201-b69c-69e0c1e6ae56",
  "output": [
    {
      "type": "message",
      "id": "msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0",
      "status": "completed",
      "role": "assistant",
      "phase": "final_answer",
      "content": [
        {
          "type": "output_text",
          "text": "The video captures a heated sideline moment during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid, visibly frustrated, and briefly bumps him before being restrained by a teammate [1].",
          "annotations": [
            {
              "type": "video_citation",
              "start_index": 211,
              "end_index": 213,
              "item_id": "ksi_069e9870-3c4d-7abc-9012-3456789abcde",
              "start_sec": 0.0,
              "end_sec": 9.0,
              "title": "Super Bowl LVIII sideline",
              "thumbnail_url": "https://example.com/thumbnail.jpg",
              "hls_url": "https://example.com/stream.m3u8"
            }
          ]
        }
      ]
    }
  ],
  "billing": {
    "amount": "0.008118",
    "currency": "USD"
  },
  "created_at": "2026-07-11T03:13:57Z"
}
```
</Accordion>

<Accordion title="Example streamed response (SSE)">
```
event: response.created
data: {"type":"response.created","sequence_number":0,"response":{"id":"resp_019f4f2a-b69e-7812-b20f-6ea6d644ceff","type":"response","object":"response","status":"in_progress","incomplete_details":null,"output":[],"session_id":"sess_019f4f2a-b69b-7a01-9018-cc51681121ea","knowledge_store_id":"ks_019ebcf4-7e08-7201-b69c-69e0c1e6ae56","created_at":"2026-07-11T03:13:47Z"}}

event: response.output_item.added
data: {"type":"response.output_item.added","sequence_number":2,"output_index":0,"item":{"type":"message","id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","status":"in_progress","role":"assistant","phase":"final_answer","content":[{"type":"output_text","text":"","annotations":[]}]}}

event: response.content_part.added
data: {"type":"response.content_part.added","sequence_number":3,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"part":{"type":"output_text","text":"","annotations":[]}}

event: response.output_text.delta
data: {"type":"response.output_text.delta","sequence_number":4,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"delta":"The video captures a heated sideline moment"}

event: response.output_text.delta
data: {"type":"response.output_text.delta","sequence_number":5,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"delta":" during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid."}

event: response.output_text.done
data: {"type":"response.output_text.done","sequence_number":124,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"text":"The video captures a heated sideline moment during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid, visibly frustrated, and briefly bumps him before being restrained by a teammate [1]."}

event: response.content_part.done
data: {"type":"response.content_part.done","sequence_number":125,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"part":{"type":"output_text","text":"The video captures a heated sideline moment during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid, visibly frustrated, and briefly bumps him before being restrained by a teammate [1].","annotations":[{"type":"url_citation","start_index":51,"end_index":66,"url":"https://example.com/news/super-bowl-lviii","title":"Super Bowl LVIII recap"},{"type":"video_citation","start_index":211,"end_index":213,"item_id":"ksi_069e9870-3c4d-7abc-9012-3456789abcde","start_sec":0.0,"end_sec":9.0,"title":"Super Bowl LVIII sideline","thumbnail_url":"https://example.com/thumbnail.jpg","hls_url":"https://example.com/stream.m3u8"}]}}

event: response.completed
data: {"type":"response.completed","sequence_number":127,"response":{"id":"resp_019f4f2a-b69e-7812-b20f-6ea6d644ceff","type":"response","object":"response","status":"completed","incomplete_details":null,"output":[{"type":"message","id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","status":"completed","role":"assistant","phase":"final_answer","content":[{"type":"output_text","text":"The video captures a heated sideline moment during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid, visibly frustrated, and briefly bumps him before being restrained by a teammate [1].","annotations":[{"type":"url_citation","start_index":51,"end_index":66,"url":"https://example.com/news/super-bowl-lviii","title":"Super Bowl LVIII recap"},{"type":"video_citation","start_index":211,"end_index":213,"item_id":"ksi_069e9870-3c4d-7abc-9012-3456789abcde","start_sec":0.0,"end_sec":9.0,"title":"Super Bowl LVIII sideline","thumbnail_url":"https://example.com/thumbnail.jpg","hls_url":"https://example.com/stream.m3u8"}]}]}],"billing":{"amount":"0.020912","currency":"USD"},"session_id":"sess_019f4f2a-b69b-7a01-9018-cc51681121ea","knowledge_store_id":"ks_019ebcf4-7e08-7201-b69c-69e0c1e6ae56","created_at":"2026-07-11T03:13:57Z"}}

data: [DONE]
```
</Accordion>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import (
    ResponseInputItem,
    ResponseToolInput_JockeyWebSearch,
    TwelveLabs,
)

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.responses.create_stream(
    knowledge_store_id="ks_019ebcf4-7e08-7201-b69c-69e0c1e6ae56",
    input=[
        ResponseInputItem(
            type="message",
            role="user",
            content="Summarize this collection and verify one claim using an official web source.",
        )
    ],
    include=["intermediate_outputs"],
    tools=[ResponseToolInput_JockeyWebSearch()],
)
for chunk in response:
    print(chunk)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store to reason over.
    
</dd>
</dl>

<dl>
<dd>

**input:** `typing.Sequence[ResponseInputItem]` 

User messages that provide context to Jockey for this request. Uses [Open Responses input item](https://www.openresponses.org/reference#input-items) conventions.
Output items cannot be submitted as input. Use `session_id` to continue a conversation.
    
</dd>
</dl>

<dl>
<dd>

**session_id:** `typing.Optional[str]` 

The session identifier for a multi-turn conversation. Pass the session identifier
returned from a previous response to continue that conversation. Omit to start
a new session.

When provided, the `knowledge_store_id` field must match the knowledge store the session
was originally created against, or the request returns `400`.
    
</dd>
</dl>

<dl>
<dd>

**instructions:** `typing.Optional[str]` — Additional guidance for Jockey, acting as a per-request system prompt.
    
</dd>
</dl>

<dl>
<dd>

**include:** `typing.Optional[typing.Sequence[ResponsesCreateStreamRequestIncludeItem]]` 

Additional items to include in the response's `output` array. By default, the `output` array contains only Jockey's final reply.

**Values**:
- `intermediate_outputs`: Also includes the steps Jockey took to produce the reply.
    
</dd>
</dl>

<dl>
<dd>

**tools:** `typing.Optional[typing.Sequence[ResponseToolInput]]` 

Tools that Jockey can use while it generates the response.
Include `{ "type": "jockey:web_search" }` to allow web search. Jockey decides
whether to use an available tool, so enabling web search does not guarantee
a search. To make a search more likely, explicitly tell Jockey what
information to look up in `input` or `instructions`.

A prompt that asks Jockey to search the web does not enable web search by
itself. If you omit `tools` or pass `null` or `[]`, Jockey cannot search
public web sources, even when the prompt requests it. The `tools` setting
applies to each request on its own, including requests that continue a
session.

This list does not control Jockey's built-in knowledge store operations.
If a requested tool is unavailable for the request, the request fails
with HTTP `422` and code `parameter_invalid`. Remove the unavailable
tool from the `tools` array and retry.
    
</dd>
</dl>

<dl>
<dd>

**selections:** `typing.Optional[typing.Sequence[ResponseSelection]]` 

Restricts the request to specific knowledge store items or item collections. The restriction is applied at the prompt level; the knowledge store does not block access to other items. Treat it as a strong preference, not a hard access boundary. Omit to run against every item.

Selections persist in the session context, and selections sent on later turns are added to that context. You can reference selections from earlier turns in natural language without repeating their `{{sel:N}}` tokens.
    
</dd>
</dl>

<dl>
<dd>

**text:** `typing.Optional[TextParam]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.responses.<a href="src/twelvelabs/responses/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method uses [Jockey](/v1.3/agents/concepts/jockey) to reason over content in a knowledge store and create a response. It uses [Open Responses](https://www.openresponses.org/specification) conventions for input items and streaming events.

Before you use this method, you must create an asset, create a knowledge store, and add the asset to the knowledge store as an item.

**Multi-turn conversations**: Supported via a session identifier. The first request implicitly creates a session; subsequent requests pass the returned identifier to continue the conversation.

**Selections**: By default, Jockey reasons over every item in the knowledge store. To narrow the scope, set the optional `selections` parameter to specific items or item collections, then reference each one with a `{{sel:N}}` token in the `content` field of an `input` item (`N` is the zero-based position in the `selections` array). The narrowing is applied at the prompt level; the knowledge store does not block access to other items.

**Streaming**: Set the `stream` parameter to `true` to receive the response as [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) (SSE). The reply streams in as a sequence of typed events and ends with a `data: [DONE]` message.

**Web sources**: Jockey can search public web sources while it generates a response. To allow this, include `{ "type": "jockey:web_search" }` in the `tools` array. The response can then cite these sources alongside content from the knowledge store, as `url_citation` annotations. Jockey decides whether to use an available tool, so enabling web search does not guarantee a search. To make a search more likely, explicitly tell Jockey what information to look up in `input` or `instructions`. A prompt that asks Jockey to search the web does not enable web search by itself. If you omit `tools` or pass `[]`, Jockey cannot search public web sources, even when the prompt requests it.

<Accordion title="Example response">
```json
{
  "id": "resp_019f4f2a-b69e-7812-b20f-6ea6d644ceff",
  "type": "response",
  "object": "response",
  "status": "completed",
  "incomplete_details": null,
  "session_id": "sess_019f4f2a-b69b-7a01-9018-cc51681121ea",
  "knowledge_store_id": "ks_019ebcf4-7e08-7201-b69c-69e0c1e6ae56",
  "output": [
    {
      "type": "message",
      "id": "msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0",
      "status": "completed",
      "role": "assistant",
      "phase": "final_answer",
      "content": [
        {
          "type": "output_text",
          "text": "The video captures a heated sideline moment during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid, visibly frustrated, and briefly bumps him before being restrained by a teammate [1].",
          "annotations": [
            {
              "type": "video_citation",
              "start_index": 211,
              "end_index": 213,
              "item_id": "ksi_069e9870-3c4d-7abc-9012-3456789abcde",
              "start_sec": 0.0,
              "end_sec": 9.0,
              "title": "Super Bowl LVIII sideline",
              "thumbnail_url": "https://example.com/thumbnail.jpg",
              "hls_url": "https://example.com/stream.m3u8"
            }
          ]
        }
      ]
    }
  ],
  "billing": {
    "amount": "0.008118",
    "currency": "USD"
  },
  "created_at": "2026-07-11T03:13:57Z"
}
```
</Accordion>

<Accordion title="Example streamed response (SSE)">
```
event: response.created
data: {"type":"response.created","sequence_number":0,"response":{"id":"resp_019f4f2a-b69e-7812-b20f-6ea6d644ceff","type":"response","object":"response","status":"in_progress","incomplete_details":null,"output":[],"session_id":"sess_019f4f2a-b69b-7a01-9018-cc51681121ea","knowledge_store_id":"ks_019ebcf4-7e08-7201-b69c-69e0c1e6ae56","created_at":"2026-07-11T03:13:47Z"}}

event: response.output_item.added
data: {"type":"response.output_item.added","sequence_number":2,"output_index":0,"item":{"type":"message","id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","status":"in_progress","role":"assistant","phase":"final_answer","content":[{"type":"output_text","text":"","annotations":[]}]}}

event: response.content_part.added
data: {"type":"response.content_part.added","sequence_number":3,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"part":{"type":"output_text","text":"","annotations":[]}}

event: response.output_text.delta
data: {"type":"response.output_text.delta","sequence_number":4,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"delta":"The video captures a heated sideline moment"}

event: response.output_text.delta
data: {"type":"response.output_text.delta","sequence_number":5,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"delta":" during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid."}

event: response.output_text.done
data: {"type":"response.output_text.done","sequence_number":124,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"text":"The video captures a heated sideline moment during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid, visibly frustrated, and briefly bumps him before being restrained by a teammate [1]."}

event: response.content_part.done
data: {"type":"response.content_part.done","sequence_number":125,"item_id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","output_index":0,"content_index":0,"part":{"type":"output_text","text":"The video captures a heated sideline moment during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid, visibly frustrated, and briefly bumps him before being restrained by a teammate [1].","annotations":[{"type":"url_citation","start_index":51,"end_index":66,"url":"https://example.com/news/super-bowl-lviii","title":"Super Bowl LVIII recap"},{"type":"video_citation","start_index":211,"end_index":213,"item_id":"ksi_069e9870-3c4d-7abc-9012-3456789abcde","start_sec":0.0,"end_sec":9.0,"title":"Super Bowl LVIII sideline","thumbnail_url":"https://example.com/thumbnail.jpg","hls_url":"https://example.com/stream.m3u8"}]}}

event: response.completed
data: {"type":"response.completed","sequence_number":127,"response":{"id":"resp_019f4f2a-b69e-7812-b20f-6ea6d644ceff","type":"response","object":"response","status":"completed","incomplete_details":null,"output":[{"type":"message","id":"msg_sess_019f4f2a-b69b-7a01-9018-cc51681121ea_0","status":"completed","role":"assistant","phase":"final_answer","content":[{"type":"output_text","text":"The video captures a heated sideline moment during Super Bowl LVIII: after a fumble, Travis Kelce approaches head coach Andy Reid, visibly frustrated, and briefly bumps him before being restrained by a teammate [1].","annotations":[{"type":"url_citation","start_index":51,"end_index":66,"url":"https://example.com/news/super-bowl-lviii","title":"Super Bowl LVIII recap"},{"type":"video_citation","start_index":211,"end_index":213,"item_id":"ksi_069e9870-3c4d-7abc-9012-3456789abcde","start_sec":0.0,"end_sec":9.0,"title":"Super Bowl LVIII sideline","thumbnail_url":"https://example.com/thumbnail.jpg","hls_url":"https://example.com/stream.m3u8"}]}]}],"billing":{"amount":"0.020912","currency":"USD"},"session_id":"sess_019f4f2a-b69b-7a01-9018-cc51681121ea","knowledge_store_id":"ks_019ebcf4-7e08-7201-b69c-69e0c1e6ae56","created_at":"2026-07-11T03:13:57Z"}}

data: [DONE]
```
</Accordion>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import (
    ResponseInputItem,
    ResponseToolInput_JockeyWebSearch,
    TwelveLabs,
)

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.responses.create(
    knowledge_store_id="ks_019ebcf4-7e08-7201-b69c-69e0c1e6ae56",
    input=[
        ResponseInputItem(
            type="message",
            role="user",
            content="Summarize this collection and verify one claim using an official web source.",
        )
    ],
    include=["intermediate_outputs"],
    tools=[ResponseToolInput_JockeyWebSearch()],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_store_id:** `str` — The unique identifier of the knowledge store to reason over.
    
</dd>
</dl>

<dl>
<dd>

**input:** `typing.Sequence[ResponseInputItem]` 

User messages that provide context to Jockey for this request. Uses [Open Responses input item](https://www.openresponses.org/reference#input-items) conventions.
Output items cannot be submitted as input. Use `session_id` to continue a conversation.
    
</dd>
</dl>

<dl>
<dd>

**session_id:** `typing.Optional[str]` 

The session identifier for a multi-turn conversation. Pass the session identifier
returned from a previous response to continue that conversation. Omit to start
a new session.

When provided, the `knowledge_store_id` field must match the knowledge store the session
was originally created against, or the request returns `400`.
    
</dd>
</dl>

<dl>
<dd>

**instructions:** `typing.Optional[str]` — Additional guidance for Jockey, acting as a per-request system prompt.
    
</dd>
</dl>

<dl>
<dd>

**include:** `typing.Optional[typing.Sequence[ResponsesCreateRequestIncludeItem]]` 

Additional items to include in the response's `output` array. By default, the `output` array contains only Jockey's final reply.

**Values**:
- `intermediate_outputs`: Also includes the steps Jockey took to produce the reply.
    
</dd>
</dl>

<dl>
<dd>

**tools:** `typing.Optional[typing.Sequence[ResponseToolInput]]` 

Tools that Jockey can use while it generates the response.
Include `{ "type": "jockey:web_search" }` to allow web search. Jockey decides
whether to use an available tool, so enabling web search does not guarantee
a search. To make a search more likely, explicitly tell Jockey what
information to look up in `input` or `instructions`.

A prompt that asks Jockey to search the web does not enable web search by
itself. If you omit `tools` or pass `null` or `[]`, Jockey cannot search
public web sources, even when the prompt requests it. The `tools` setting
applies to each request on its own, including requests that continue a
session.

This list does not control Jockey's built-in knowledge store operations.
If a requested tool is unavailable for the request, the request fails
with HTTP `422` and code `parameter_invalid`. Remove the unavailable
tool from the `tools` array and retry.
    
</dd>
</dl>

<dl>
<dd>

**selections:** `typing.Optional[typing.Sequence[ResponseSelection]]` 

Restricts the request to specific knowledge store items or item collections. The restriction is applied at the prompt level; the knowledge store does not block access to other items. Treat it as a strong preference, not a hard access boundary. Omit to run against every item.

Selections persist in the session context, and selections sent on later turns are added to that context. You can reference selections from earlier turns in natural language without repeating their `{{sel:N}}` tokens.
    
</dd>
</dl>

<dl>
<dd>

**text:** `typing.Optional[TextParam]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Data connectors
<details><summary><code>client.data_connectors.<a href="src/twelvelabs/data_connectors/client.py">authorize_connection</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method starts the OAuth authorization flow for a data connector. The platform returns an authorization URL. Redirect the user to this URL so they can grant access to their account.

After the user grants or denies access, the platform redirects them to the redirect URI you provided, with the outcome appended to that URI as query parameters. Read these parameters from the redirect that your application receives:

- `connection_id`: The identifier of the new connection, returned on success. Store this value and pass it as the `connection_id` path parameter in later requests.
- `status`: The `ok` value, returned on success.
- `custom_id`: The label you supplied, returned on success when you provided one.
- `error`: An error code, returned instead of the other parameters when the user denies access or the flow fails.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.data_connectors.authorize_connection(
    provider="google_drive",
    redirect_uri="https://app.example.com/oauth/done",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**provider:** `AuthorizeConnectionRequestProvider` — The data connector provider to authorize.
    
</dd>
</dl>

<dl>
<dd>

**redirect_uri:** `str` — The URI where the user is redirected after granting or denying access. By default, any redirect URI is accepted. If you've authorized specific redirect URIs with the [Register a redirect URI](/v1.3/api-reference/data-connectors/register-a-redirect-uri) method, this URI must be one of them.
    
</dd>
</dl>

<dl>
<dd>

**custom_id:** `typing.Optional[str]` — A label you supplied, stored on the connection and returned with it. Use a value that does not identify a person so you can match the connection to your own records.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.data_connectors.<a href="src/twelvelabs/data_connectors/client.py">list_connections</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of the connections in your account. The platform returns your connections sorted by creation date, with the newest at the top of the list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.data_connectors.list_connections(
    page=1,
    page_limit=10,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.data_connectors.<a href="src/twelvelabs/data_connectors/client.py">retrieve_connection</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves details about the specified connection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.data_connectors.retrieve_connection(
    connection_id="665f0a2c9b1e4d0012a3f7c9",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connection_id:** `str` — The unique identifier of the connection to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.data_connectors.<a href="src/twelvelabs/data_connectors/client.py">delete_connection</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method disconnects the specified connection. The platform revokes access at the provider and deletes the stored tokens. Assets imported through this connection are retained.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.data_connectors.delete_connection(
    connection_id="665f0a2c9b1e4d0012a3f7c9",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connection_id:** `str` — The unique identifier of the connection to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.data_connectors.<a href="src/twelvelabs/data_connectors/client.py">create_connection_picker_token</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method generates a short-lived, read-only access token that you use with the provider's file picker, such as the Google Drive Picker. The platform never returns the refresh token of the connection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.data_connectors.create_connection_picker_token(
    connection_id="665f0a2c9b1e4d0012a3f7c9",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connection_id:** `str` — The unique identifier of the connection.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.data_connectors.<a href="src/twelvelabs/data_connectors/client.py">list_redirect_uris</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns your authorized redirect URIs, sorted by creation date with the newest at the top. Each one is a redirect URI the [Authorize a connection](/v1.3/api-reference/data-connectors/authorize-a-connection) method accepts.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.data_connectors.list_redirect_uris(
    page=1,
    page_limit=10,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.data_connectors.<a href="src/twelvelabs/data_connectors/client.py">create_redirect_uri</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method registers a redirect URI so the [Authorize a connection](/v1.3/api-reference/data-connectors/authorize-a-connection) method accepts it.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.data_connectors.create_redirect_uri(
    redirect_uri="https://app.example.com/oauth/done",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**redirect_uri:** `str` — The redirect URI to register. Must use HTTPS, resolve to a public host, and contain no wildcards. Register it exactly as your application sends it, because the authorization flow requires an exact match.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.data_connectors.<a href="src/twelvelabs/data_connectors/client.py">delete_redirect_uri</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method removes a redirect URI from your authorized redirect URIs. After deletion, the [Authorize a connection](/v1.3/api-reference/data-connectors/authorize-a-connection) method no longer accepts it. This action cannot be undone.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.data_connectors.delete_redirect_uri(
    redirect_uri_id="665f0a2c9b1e4d0012a3f7c9",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**redirect_uri_id:** `str` — The unique identifier of the redirect URI to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Imports
<details><summary><code>client.imports.<a href="src/twelvelabs/imports/client.py">list_imports</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of the imports for the specified connection. The platform returns the imports sorted by creation date, with the newest at the top of the list. Each import in the list is a summary and does not include the per-file details. To see them, use the [Retrieve an import](/v1.3/api-reference/data-connectors/imports/retrieve-an-import) endpoint.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.imports.list_imports(
    connection_id="665f0a2c9b1e4d0012a3f7c9",
    page=1,
    page_limit=10,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connection_id:** `str` — The unique identifier of the connection to list imports for.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.imports.<a href="src/twelvelabs/imports/client.py">import_files</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method imports one or more files from the connected provider account into the platform as assets. Videos can be up to 10 GB, audio up to 4 GB, and images up to 32 MB. For each newly imported file, the platform creates an asset in the `processing` status and fetches the file asynchronously. If you import a file that was already imported through this account, the platform returns the existing asset with its current status, without fetching the file again. If the earlier fetch had failed, the platform fetches the file again. The response contains one entry per requested file, in request order. Use the `action` field of each entry to identify which files were newly imported and which were already imported.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs
from twelvelabs.imports import ImportFilesRequestItemsItem

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.imports.import_files(
    connection_id="665f0a2c9b1e4d0012a3f7c9",
    items=[
        ImportFilesRequestItemsItem(
            source_id="1AbCDef_drive_file_id_x",
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connection_id:** `str` — The unique identifier of the connection to import through.
    
</dd>
</dl>

<dl>
<dd>

**items:** `typing.Sequence[ImportFilesRequestItemsItem]` — The files to import. Provide an array of one item for a single import, or multiple items for a batch import. A maximum of 100 items can be imported per request. The `source_id` field of each item must be unique within a request.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.imports.<a href="src/twelvelabs/imports/client.py">retrieve_import</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves a single import. For each file, the response includes the `action` field, which indicates the outcome of the import operation, and the `status` field, which reflects the current status of the asset each time you retrieve the import.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.imports.retrieve_import(
    connection_id="665f0a2c9b1e4d0012a3f7c9",
    import_id="665f0afe9b1e4d0012a3f7d0",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connection_id:** `str` — The unique identifier of the connection to retrieve the import from.
    
</dd>
</dl>

<dl>
<dd>

**import_id:** `str` — The unique identifier of the import to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## AnalyzeAsync Tasks
<details><summary><code>client.analyze_async.tasks.<a href="src/twelvelabs/analyze_async/tasks/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of the analysis tasks in your account. The platform returns your analysis tasks sorted by creation date, with the newest at the top of the list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze_async.tasks.list(
    page=1,
    page_limit=10,
    status="queued",
    video_url="https://example.com/video.mp4",
    asset_id="69abc123def456789012abcd",
    analysis_mode="general",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[AnalyzeTaskStatus]` 

Filter analysis tasks by status.
Possible values: `queued`, `pending`, `processing`, `ready`, `failed`, `canceled`.
    
</dd>
</dl>

<dl>
<dd>

**video_url:** `typing.Optional[str]` — Filter tasks by exact video source URL.
    
</dd>
</dl>

<dl>
<dd>

**asset_id:** `typing.Optional[str]` — Filter tasks by asset ID.
    
</dd>
</dl>

<dl>
<dd>

**analysis_mode:** `typing.Optional[TasksListRequestAnalysisMode]` — Filter tasks by the analysis mode used when creating the task.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.analyze_async.tasks.<a href="src/twelvelabs/analyze_async/tasks/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method analyzes a video or one or more images asynchronously. Each request must contain a video or one or more images, but not both.

The method supports two analysis modes:

- **General analysis**: Prompt-based text generation with a video or one or more images.
- **Video segmentation**: Timestamped metadata with custom segment definitions.

<Accordion title="Input requirements">
**Videos**
- The video can be up to 2 hours long, or up to 4 hours when you analyze only a portion of it. You can analyze between 1 second and 2 hours of the video. HLS and base64 videos are limited to 2 hours.
- Formats: [FFmpeg supported formats](https://ffmpeg.org/ffmpeg-formats.html)
- Resolution: 360x360 to 5184x2160 pixels
- Aspect ratio: Between 1:1 and 1:2.4, or between 2.4:1 and 1:1.

**Images**
- You can provide one to twenty images per request.
- Formats: JPEG, PNG, WebP, GIF, and BMP.
- Maximum size: 20 MB per image.
- Maximum pixel count: 16,777,216 pixels per image (width × height).
</Accordion>

**When to use this method**:
- Generate custom text from your video or one or more images using a prompt (general analysis)
- Extract timestamped metadata with custom segment definitions from your video
- Analyze videos longer than 1 hour, or a portion of a video up to 4 hours long
- Process videos or images asynchronously without blocking your application

**Do not use this method for**:
- Videos or images for which you need immediate results or real-time streaming. Use the [`POST`](/v1.3/api-reference/analyze-videos/sync-analysis) method of the `/analyze` endpoint instead.

Analyzing content asynchronously requires three steps:

1. Create an analysis task using this method. The platform returns a task identifier.
2. Poll the status of the task using the [`GET`](/v1.3/api-reference/analyze-videos/retrieve-analysis-task-status-results) method of the `/analyze/tasks/{task_id}` endpoint. Wait until the status is `ready`, `failed`, or `canceled`.
3. When the status is `ready`, retrieve the results using the [`GET`](/v1.3/api-reference/analyze-videos/retrieve-analysis-task-status-results) method of the `/analyze/tasks/{task_id}` endpoint.

On the Free plan, you have a total of 600 minutes (10 hours) shared across indexing, analysis, and segmentation. For details, see the [Video hours and video count limits](/v1.3/docs/concepts/indexes#video-hours-and-video-count-limits) section.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import AsyncResponseFormat, TwelveLabs, VideoContext_Url

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze_async.tasks.create(
    model_name="pegasus1.5",
    video=VideoContext_Url(
        url="https://example.com/video.mp4",
    ),
    prompt="Identify intro, main content, and outro clips.",
    response_format=AsyncResponseFormat(
        type="json_schema",
        json_schema={
            "type": "object",
            "properties": {
                "clip_start": {"type": "timestamp", "format": "seconds"},
                "events": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "intro_end": {
                                "type": "timestamp",
                                "format": "hh:mm:ss",
                            },
                            "outro_start": {
                                "type": "timestamp",
                                "format": "hh:mm:ss.fff",
                            },
                            "label": {"type": "string"},
                        },
                    },
                },
            },
        },
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_name:** `typing.Optional[CreateAsyncAnalyzeRequestModelName]` 

The video understanding model to use for analysis.
- `pegasus1.6`: For details about this version, see the [Pegasus 1.6](/v1.3/docs/concepts/models/pegasus/pegasus-1-6) page.
- `pegasus1.5`: For details about this version, see the [Pegasus 1.5](/v1.3/docs/concepts/models/pegasus/pegasus-1-5) page.

**Default:** `pegasus1.5`
    
</dd>
</dl>

<dl>
<dd>

**custom_id:** `typing.Optional[str]` 

An optional identifier that you set when you create the task. Use this field to correlate tasks across responses, for example, to distinguish tasks by type or environment.

The platform stores this value unchanged and returns it in the following responses:
- The [`GET`](/v1.3/api-reference/analyze-videos/retrieve-analysis-task-status-results) method of the `/analyze/tasks/{task_id}` endpoint
- The [`GET`](/v1.3/api-reference/analyze-videos/list-async-analysis-tasks) method of the `/analyze/tasks` endpoint
- The `analyze.task.ready`, `analyze.task.failed`, and `analyze.task.canceled` webhook payloads

**Format**: 1–64 characters. Alphanumeric, hyphens (`-`), and underscores (`_`) only. An empty string is rejected with a `400 Bad Request`.

This field does not enforce uniqueness. You can submit multiple tasks with the same `custom_id`. To prevent duplicate task creation, use an `Idempotency-Key` header instead.
    
</dd>
</dl>

<dl>
<dd>

**video:** `typing.Optional[VideoContext]` 
    
</dd>
</dl>

<dl>
<dd>

**image:** `typing.Optional[typing.Sequence[AnalyzeImageInput]]` 

A list of up to twenty objects containing the images to analyze. For each image, include exactly one source. Requires Pegasus 1.6. Using any other model returns a `parameter_invalid` error.

Mutually exclusive with the `video` and `prompt_v2` parameters. The `prompt` parameter is required when you provide images.
    
</dd>
</dl>

<dl>
<dd>

**prompt:** `typing.Optional[str]` 

Natural-language instructions for analyzing the video or one or more images. Required for general analysis (prompt-based text generation). Not supported when `analysis_mode` is `time_based_metadata`. To include reference images in your prompt, use the `prompt_v2` parameter instead. Mutually exclusive with the `prompt_v2` parameter.

Your prompts can be instructive or descriptive, or you can phrase them as questions. This text counts toward the [context window](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#context-window).

**Examples**:

- Based on this video, I want to generate five keywords for SEO (Search Engine Optimization).
- I want to generate a description for my video with the following format: Title of the video, followed by a summary in 2-3 sentences, highlighting the main topic, key events, and concluding remarks.
    
</dd>
</dl>

<dl>
<dd>

**prompt_v_2:** `typing.Optional[AnalyzePromptV2]` 

A structured prompt that uses `<@name>` placeholders to reference images. Mutually exclusive with the `prompt` and `image` parameters.

The prompt text and reference images count toward the [context window](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#context-window).
    
</dd>
</dl>

<dl>
<dd>

**analysis_mode:** `typing.Optional[CreateAsyncAnalyzeRequestAnalysisMode]` 

The analysis mode for this task.
- `general`: Analyze the video and generate a response based on your prompt. Supports both free-form text and structured output via `response_format`.
- `time_based_metadata`: Segment the video into time-based intervals and extract custom metadata for each segment. Requires `response_format.type` set to `segment_definitions`.

**Default:** `general`
    
</dd>
</dl>

<dl>
<dd>

**temperature:** `typing.Optional[AnalyzeTemperature]` 
    
</dd>
</dl>

<dl>
<dd>

**max_tokens:** `typing.Optional[CreateAsyncAnalyzeRequestMaxTokens]` 

The maximum response length, in tokens. Provide an integer or the `unlimited` value.

The allowed integer range and default depend on the analysis mode:

| Mode | Min | Max | Default |
|------|-----|-----|---------|
| `general` | 512 | 98,304 | 4,096 |
| `time_based_metadata` | 2,048 | 98,304 | 32,768 |

- **Integer**: With video segmentation, the task fails if the output exceeds the limit. No partial output is returned.
- **Unlimited**: Removes the token limit from video segmentation. It requires `analysis_mode` set to `time_based_metadata` and `model_name` set to `pegasus1.6`. Mutually exclusive with `response_format.segment_definitions[].time_ranges`.

  The platform extracts as many segments as it can. If it stops before extracting every segment, the task still completes with the `status` field set to `ready`. The `error` field contains the warning that the results may be incomplete.
    
</dd>
</dl>

<dl>
<dd>

**response_format:** `typing.Optional[AsyncResponseFormat]` 
    
</dd>
</dl>

<dl>
<dd>

**min_segment_duration:** `typing.Optional[float]` 

Minimum duration for each extracted segment, in seconds. Set this value to enforce a minimum segment length. Requires `analysis_mode` set to `time_based_metadata`. Mutually exclusive with `response_format.segment_definitions[].time_ranges`.

**Min:** 2
    
</dd>
</dl>

<dl>
<dd>

**max_segment_duration:** `typing.Optional[float]` 

Maximum duration for each extracted segment, in seconds. Set this value to split long continuous sections into shorter segments. Must be greater than or equal to `min_segment_duration`. Requires `analysis_mode` set to `time_based_metadata`. Mutually exclusive with `response_format.segment_definitions[].time_ranges`.

**Min:** 2
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `typing.Optional[float]` 

Start of the analysis window, as an absolute timestamp in seconds, based on the internal metadata of the video. Use with `end_time` to analyze only a portion of the video.

<Note title="Notes">
- If omitted, defaults to the internal start time of the video.
- Most videos start at 0, but some (for example, from cameras or broadcast recordings) may have a non-zero start time. To find the value, run `ffprobe -v error -show_entries format=start_time,duration -of default=noprint_wrappers=1 your_video.mp4`.
- Must be less than `end_time` and the video duration.
- The window (`end_time - start_time`) must be at least 1 second and at most 2 hours. The video may be up to 4 hours as long as the window stays within that limit.
- Mutually exclusive with `response_format.segment_definitions[].time_ranges`.
- Together with `end_time`, this parameter determines the billable video duration. If you omit both, billing uses the full video duration. For details, see the [Frequently asked questions](/v1.3/docs/resources/frequently-asked-questions#how-is-video-segmentation-priced) page.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[float]` 

End of the analysis window, as an absolute timestamp in seconds, based on the internal metadata of the video. Use with `start_time` to analyze only a portion of the video.

<Note title="Notes">
- If omitted, defaults to the internal start time of the video plus its duration.
- Most videos start at 0, but some (for example, from cameras or broadcast recordings) may have a non-zero start time. To find the value, run `ffprobe -v error -show_entries format=start_time,duration -of default=noprint_wrappers=1 your_video.mp4`.
- Must be greater than `start_time` and less than or equal to the video duration.
- The window (`end_time - start_time`) must be at least 1 second and at most 2 hours. The video may be up to 4 hours as long as the window stays within that limit.
- Mutually exclusive with `response_format.segment_definitions[].time_ranges`.
- Together with `start_time`, this parameter determines the billable video duration. If you omit both, billing uses the full video duration. For details, see the [Frequently asked questions](/v1.3/docs/resources/frequently-asked-questions#how-is-video-segmentation-priced) page.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.analyze_async.tasks.<a href="src/twelvelabs/analyze_async/tasks/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves the status and results of an analysis task.

**Task statuses**:
- `queued`: The task is waiting to be processed.
- `pending`: The task is queued and waiting to start.
- `processing`: The platform is analyzing the video.
- `ready`: Processing is complete. Results are available in the response.
- `failed`: The task failed. No result is available. The `error` field describes the failure.
- `canceled`: The task was canceled. No result is available. The `error` field describes the cancellation reason, if available.

Poll this method until `status` is `ready`, `failed`, or `canceled`. When `status` is `ready`, use the results from the response.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze_async.tasks.retrieve(
    task_id="64f8d2c7e4a1b37f8a9c5d12",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**task_id:** `str` — The unique identifier of the analysis task.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.analyze_async.tasks.<a href="src/twelvelabs/analyze_async/tasks/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes an analysis task. You can only delete tasks that are not currently being processed.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze_async.tasks.delete(
    task_id="64f8d2c7e4a1b37f8a9c5d12",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**task_id:** `str` — The unique identifier of the analyze task.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.analyze_async.tasks.<a href="src/twelvelabs/analyze_async/tasks/client.py">cancel</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to cancel an asynchronous analysis task in your account. To cancel a task created as part of a batch, use the [`POST`](/v1.3/api-reference/analyze-videos/batch-analysis/cancel-batch) method of the `/analyze/batches/{batch_id}/cancel` endpoint.

You can cancel a task with the `queued`, `pending`, or `processing` status. This action cannot be undone.

Processing that has already started can continue briefly after cancellation.

When you cancel a task, the platform can send an `analyze.task.canceled` webhook. Delivery is best-effort: a `200` response is not a delivery guarantee. When you receive the event, retrieve the task for its current state.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze_async.tasks.cancel(
    task_id="64f8d2c7e4a1b37f8a9c5d12",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**task_id:** `str` — The unique identifier of the analysis task you want to cancel.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## AnalyzeAsync Batches
<details><summary><code>client.analyze_async.batches.<a href="src/twelvelabs/analyze_async/batches/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to list all the batch objects in your account. The response sorts batches by creation date, with the newest batch first.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.analyze_async.batches.list(
    page=1,
    page_limit=10,
    status=["processing", "canceling"],
    analysis_mode=["general", "time_based_metadata"],
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[typing.Union[BatchStatus, typing.Sequence[BatchStatus]]]` 

Filter batches by status. Provide one or more values to include batches matching any of them. To send multiple values, repeat the `status` parameter:
```
status=processing&status=canceling
```
If you omit this parameter, the response includes batches in all statuses.
    
</dd>
</dl>

<dl>
<dd>

**analysis_mode:** `typing.Optional[
    typing.Union[
        BatchesListRequestAnalysisModeItem,
        typing.Sequence[BatchesListRequestAnalysisModeItem],
    ]
]` 

Filter batches by analysis mode. Provide one or more values to include batches matching any of them. To send multiple values, repeat the `analysis_mode` parameter:
```
analysis_mode=general&analysis_mode=time_based_metadata
```
If you omit this parameter, the response includes batches in all analysis modes.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.analyze_async.batches.<a href="src/twelvelabs/analyze_async/batches/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to submit many video analysis requests in a single call. Each request creates an analysis task. The response contains one batch identifier and one task identifier per request. Use the batch identifier to check progress and retrieve results.

**When to use this method**:
- Run the same analysis settings across many videos.
- Track a single batch instead of many individual analysis tasks.

**Do not use this method for**:
- Single videos that require immediate results. Use the [`POST`](/v1.3/api-reference/analyze-videos/sync-analysis) method of the `/analyze` endpoint instead.
- Background processing of a single video. Use the [`POST`](/v1.3/api-reference/analyze-videos/create-async-analysis-task) method of the `/analyze/tasks` endpoint instead.

**Retention and retry**:
- Batches expire 24 hours after creation. You can retrieve results for 30 days after creation.
- If processing does not finish for some items in time, resubmit them in a new batch.
- An item whose analysis window exceeds 2 hours fails on its own. The error code is `video_duration_too_long`. The rest of the batch is still submitted.

**Limits**:
- Up to 1,000 requests per batch.
- Up to 2,000 total content hours per batch.
- Up to 5 active batches per account.
- The duration limits of the [`POST`](/v1.3/api-reference/analyze-videos/create-async-analysis-task) method of the `/analyze/tasks` endpoint apply to each item.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import (
    AsyncResponseFormat,
    BatchDefaults,
    BatchItemRequest,
    BatchVideoContext,
    SegmentDefinition,
    SegmentField,
    SmeMediaSource,
    TwelveLabs,
)

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze_async.batches.create(
    model_name="pegasus1.5",
    analysis_mode="time_based_metadata",
    defaults=BatchDefaults(
        response_format=AsyncResponseFormat(
            type="segment_definitions",
            segment_definitions=[
                SegmentDefinition(
                    id="product_moments",
                    description="Moments where a person holds <@product> while speaking to the camera.",
                    fields=[
                        SegmentField(
                            name="segment_title",
                            type="string",
                            description="A short headline for this moment",
                        ),
                        SegmentField(
                            name="product_visibility",
                            type="string",
                            description="How prominently the product appears in this segment",
                            enum=["FULL", "PARTIAL", "BACKGROUND"],
                        ),
                    ],
                    media_sources=[
                        SmeMediaSource(
                            name="product",
                            media_type="image",
                            url="https://example.com/product.jpg",
                        )
                    ],
                )
            ],
        ),
        temperature=0.0,
        max_tokens=4096,
        min_segment_duration=2.0,
    ),
    requests=[
        BatchItemRequest(
            video=BatchVideoContext(
                type="asset_id",
                asset_id="6298d673f1090f1100476d4c",
            ),
            custom_id="ep-001",
        ),
        BatchItemRequest(
            video=BatchVideoContext(
                type="asset_id",
                asset_id="6298d673f1090f1100476d4d",
            ),
            custom_id="ep-002",
        ),
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_name:** `CreateAnalyzeBatchRequestModelName` — The video understanding model to use for every item in this batch.
    
</dd>
</dl>

<dl>
<dd>

**analysis_mode:** `CreateAnalyzeBatchRequestAnalysisMode` 

The analysis mode for every item in this batch.
- `general`: Generate text from each video based on the prompt (the `prompt` field of the item if set, otherwise `defaults.prompt`). Supports structured JSON output by using `json_schema` in the `response_format.type` field.
- `time_based_metadata`: Extract timestamped metadata by using `segment_definitions` in the `response_format.type` field.

Batches with mixed modes are not supported.
    
</dd>
</dl>

<dl>
<dd>

**requests:** `typing.Sequence[BatchItemRequest]` — The analysis requests in the batch. Provide 1 to 1,000 requests, with a combined video duration of up to 2,000 hours.
    
</dd>
</dl>

<dl>
<dd>

**defaults:** `typing.Optional[BatchDefaults]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.analyze_async.batches.<a href="src/twelvelabs/analyze_async/batches/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to monitor a batch. The response includes the current batch status and counts for queued, processing, ready, failed, and canceled items.

Poll this method until the batch reaches the `completed`, `canceled`, or `expired` status. To retrieve the results, call the [`GET`](/v1.3/api-reference/analyze-videos/batch-analysis/retrieve-batch-results) method of the `/analyze/batches/{batch_id}/results` endpoint.

Do not treat the `completed` status as a success signal. It means processing has finished for every item, not that every analysis succeeded. To see how many items succeeded, failed, or were canceled, check the `ready_items`, `failed_items`, and `canceled_items` fields. A batch never has the `failed` status.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze_async.batches.retrieve(
    batch_id="68f4ddaf8aaa60d33df0e800",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**batch_id:** `str` — The unique identifier of the batch.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.analyze_async.batches.<a href="src/twelvelabs/analyze_async/batches/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to delete a batch and all the tasks associated with it. You can only delete batches with status `completed`, `canceled`, or `expired`.

Deleting a batch does not affect billing. You are billed for every completed analysis regardless of whether you delete the batch afterward.

To stop a batch with the `pending` or `processing` status, use the [`POST`](/v1.3/api-reference/analyze-videos/batch-analysis/cancel-batch) method of the `/analyze/batches/{batch_id}/cancel` endpoint.

Batches are deleted 30 days after creation.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze_async.batches.delete(
    batch_id="68f4ddaf8aaa60d33df0e800",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**batch_id:** `str` — The unique identifier of the batch.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.analyze_async.batches.<a href="src/twelvelabs/analyze_async/batches/client.py">results</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to retrieve the results for each item in a batch. You can call it while the batch has the `pending` or `processing` status.

Each result entry has a status. For details on each status, see the [Item statuses](/v1.3/api-reference/analyze-videos/batch-analysis/the-batch-object#item-statuses) section on the **The batch object** page.

Each result entry includes a task identifier in the `task_id` field. Use this value with the [`GET`](/v1.3/api-reference/analyze-videos/retrieve-analysis-task-status-results) method of the `/analyze/tasks/{task_id}` endpoint if you need the full analysis task response.

You can retrieve results for 30 days after batch creation.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.analyze_async.batches.results(
    batch_id="68f4ddaf8aaa60d33df0e800",
)
for chunk in response:
    print(chunk)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**batch_id:** `str` — The unique identifier of the batch.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.analyze_async.batches.<a href="src/twelvelabs/analyze_async/batches/client.py">cancel</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to request cancellation for a batch with the `pending` or `processing` status.

When you invoke this method, the platform performs the following steps:
- Cancels the items in the `queued` status.
- Finishes the analysis for the items in the `processing` status.

The batch status changes to `canceling` immediately, and to `canceled` after every item reaches `ready`, `failed`, or `canceled`. You are not billed for canceled or failed items.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.analyze_async.batches.cancel(
    batch_id="68f4ddaf8aaa60d33df0e800",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**batch_id:** `str` — The unique identifier of the batch.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Embed Tasks
<details><summary><code>client.embed.tasks.<a href="src/twelvelabs/embed/tasks/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Note title="Note">
  This method will be deprecated in a future version. Migrate to the [Embed API v2](/v1.3/api-reference/create-embeddings-v2) for continued support and access to new features.
</Note>
This method returns a list of the video embedding tasks in your account. The platform returns your video embedding tasks sorted by creation date, with the newest at the top of the list.

<Note title="Notes">
- Video embeddings are stored for seven days.
- When you invoke this method without specifying the `started_at` and `ended_at` parameters, the platform returns all the video embedding tasks created within the last seven days.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.embed.tasks.list(
    started_at="2024-03-01T00:00:00Z",
    ended_at="2024-03-01T00:00:00Z",
    status="processing",
    page=1,
    page_limit=10,
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**started_at:** `typing.Optional[str]` — Retrieve the embedding tasks that were created at or after the given date and time, expressed in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ").
    
</dd>
</dl>

<dl>
<dd>

**ended_at:** `typing.Optional[str]` — Retrieve the embedding tasks that were created at or before the given date and time, expressed in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ").
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[str]` 

Filter the embedding tasks by their current status.

**Values**: `processing`, `ready`, or `failed`.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.tasks.<a href="src/twelvelabs/embed/tasks/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>


<Note title="Note">
  This endpoint will be deprecated in a future version. Migrate to the [Embed API v2](/v1.3/api-reference/create-embeddings-v2) for continued support and access to new features.
</Note>

This method creates a new video embedding task that uploads a video to the platform and creates one or multiple video embeddings.

<Note title="Note">
This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
</Note>

Upload options:
- **Local file**: Use the `video_file` parameter
- **Publicly accessible URL**: Use the `video_url` parameter.

Specify at least one option. If both are provided, `video_url` takes precedence.

Your videos must meet the [requirements](/v1.3/docs/concepts/models/marengo/marengo-3-0#video-file-requirements).
This endpoint allows you to upload files up to 2 GB in size.  To upload larger files, use the [Multipart Upload API](/v1.3/api-reference/upload-content/multipart-uploads)

<Note title="Notes">
- The Marengo video understanding model generates embeddings for all modalities in the same latent space. This shared space enables any-to-any searches across different types of content.
- Video embeddings are stored for seven days.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.tasks.create(
    model_name="model_name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_name:** `str` 

The name of the model you want to use. The following models are available:
  - `marengo3.0`: Enhanced model with sports intelligence and extended content support.
    
</dd>
</dl>

<dl>
<dd>

**video_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**video_url:** `typing.Optional[str]` — Specify this parameter to upload a video from a publicly accessible URL.
    
</dd>
</dl>

<dl>
<dd>

**video_start_offset_sec:** `typing.Optional[float]` 

The start offset in seconds from the beginning of the video where processing should begin. Specifying 0 means starting from the beginning of the video.

**Default**: 0
**Min**: 0
**Max**: Duration of the video minus video_clip_length
    
</dd>
</dl>

<dl>
<dd>

**video_end_offset_sec:** `typing.Optional[float]` 

The end offset in seconds from the beginning of the video where processing should stop.

Ensure the following when you specify this parameter:
- The end offset does not exceed the total duration of the video file.
- The end offset is greater than the start offset.
- You must set both the start and end offsets. Setting only one of these offsets is not permitted, resulting in an error.

**Min**: video_start_offset + video_clip_length
**Max**: Duration of the video file
    
</dd>
</dl>

<dl>
<dd>

**video_clip_length:** `typing.Optional[float]` 

The desired duration in seconds for each clip for which the platform generates an embedding. Ensure that the clip length does not exceed the interval between the start and end offsets.

**Default**: 6
**Min**: 2
**Max**: 10
    
</dd>
</dl>

<dl>
<dd>

**video_embedding_scope:** `typing.Optional[typing.List[TasksCreateRequestVideoEmbeddingScopeItem]]` 

Defines the scope of video embedding generation. Valid values are the following:
- `clip`: Creates embeddings for each video segment of `video_clip_length` seconds, from `video_start_offset_sec` to `video_end_offset_sec`.
- `clip` and `video`: Creates embeddings for video segments and the entire video. Use the `video` scope for videos up to 10-30 seconds to maintain optimal performance.

To create embeddings for segments and the entire video in the same request, include this parameter twice as shown below:

```json
--form video_embedding_scope=clip \
--form video_embedding_scope=video
```

**Default**: `clip`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.tasks.<a href="src/twelvelabs/embed/tasks/client.py">status</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Note title="Note">
  This endpoint will be deprecated in a future version. Migrate to the [Embed API v2](/v1.3/api-reference/create-embeddings-v2) for continued support and access to new features.
</Note>
This method retrieves the status of a video embedding task. Check the task status of a video embedding task to determine when you can retrieve the embedding.

A task can have one of the following statuses:
- `processing`: The platform is creating the embeddings.
- `ready`:  Processing is complete. Retrieve the embeddings by invoking the [`GET`](/v1.3/api-reference/create-embeddings-v1/video-embeddings/retrieve-video-embeddings) method of the `/embed/tasks/{task_id} endpoint`.
- `failed`: The task could not be completed, and the embeddings haven't been created.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.tasks.status(
    task_id="663da73b31cdd0c1f638a8e6",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**task_id:** `str` — The unique identifier of your video embedding task.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.tasks.<a href="src/twelvelabs/embed/tasks/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves embeddings for a specific video embedding task. Ensure the task status is `ready` before invoking this method. Refer to the [Retrieve the status of a video embedding tasks](/v1.3/api-reference/create-embeddings-v1/video-embeddings/retrieve-video-embedding-task-status) page for instructions on checking the task status.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.tasks.retrieve(
    task_id="663da73b31cdd0c1f638a8e6",
    embedding_option=["visual"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**task_id:** `str` — The unique identifier of your video embedding task.
    
</dd>
</dl>

<dl>
<dd>

**embedding_option:** `typing.Optional[
    typing.Union[
        TasksRetrieveRequestEmbeddingOptionItem,
        typing.Sequence[TasksRetrieveRequestEmbeddingOptionItem],
    ]
]` 

Specifies which types of embeddings to retrieve. Values: `visual`, `audio`, `transcription`. For details, see the [Embedding options](/v1.3/docs/concepts/modalities#embedding-options) section.

<Note title="Note">
The platform returns all available embeddings when you omit this parameter.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Embed V2
<details><summary><code>client.embed.v_2.<a href="src/twelvelabs/embed/v_2/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method synchronously creates embeddings for multimodal content and returns the results immediately in the response.

Use this method to embed a query for retrieving matching content. With Marengo 3.5, audio and video can be up to 30 seconds. With Marengo 3.0, they can be up to 10 minutes. For longer content, use the [`POST`](/v1.3/api-reference/create-embeddings-v2/create-async-embedding-task) method of the `/embed-v2/tasks` endpoint instead.

With the Marengo 3.5 native input format, this method accepts only `multi_input`; provide text, images, audio, video, or documents as media sources. It does not accept the individual `audio` or `video` fields or a `transcription` embedding option. Marengo 3.0 and Marengo 3.5 requests using the Marengo 3.0-compatible input format accept the individual input types, including their transcription options and defaults. The API does not report which input format applies to a Marengo 3.5 request. For the formats, resolutions, file sizes, and duration limits each model accepts, see the input requirements for [Marengo 3.5](/v1.3/docs/concepts/models/marengo/marengo-3-5#input-requirements) or [Marengo 3.0](/v1.3/docs/concepts/models/marengo/marengo-3-0#input-requirements).

<Note title="Note">
This method is rate-limited. With Marengo 3.5, the platform counts input tokens for each type of content. A request can exceed a limit before you see an error. For details, see [Input token limits for embedding](/v1.3/docs/get-started/plans-and-billing/rate-limits/new-billing#input-token-limits-for-embedding).
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import MultiInputRequest, TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.v_2.create(
    input_type="multi_input",
    model_name="marengo3.5",
    multi_input=MultiInputRequest(
        input_text="man walking a dog",
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**input_type:** `CreateEmbeddingsRequestInputType` 

The type of content for the embeddings.

**Values**:
- `multi_input`: Text and up to 10 media sources, combined into a single embedding. To reference a specific media source from your text, use a placeholder in the following format: `<@name>`, where `name` matches the `name` field of a media source. The Marengo 3.5 native input format accepts images, video, audio, and documents as media sources. Marengo 3.0 and the Marengo 3.0-compatible format for Marengo 3.5 accept images.
- `audio`: An audio file. Supported with Marengo 3.0 and the Marengo 3.0-compatible input format for Marengo 3.5.
- `video`: A video file. Supported with Marengo 3.0 and the Marengo 3.0-compatible input format for Marengo 3.5.
- `image`: An image file. Supported with Marengo 3.0 and the Marengo 3.0-compatible input format for Marengo 3.5.
- `text`: Text input. Supported with Marengo 3.0 and the Marengo 3.0-compatible input format for Marengo 3.5.
- `text_image`: Text and an image. Supported with Marengo 3.0 and the Marengo 3.0-compatible input format for Marengo 3.5.
    
</dd>
</dl>

<dl>
<dd>

**model_name:** `CreateEmbeddingsRequestModelName` 

The embedding model to use.

**Values**:
- `marengo3.5`: For details about this version, see the [Marengo 3.5](/v1.3/docs/concepts/models/marengo/marengo-3-5) page.
- `marengo3.0`: For details about this version, see the [Marengo 3.0](/v1.3/docs/concepts/models/marengo/marengo-3-0) page.
    
</dd>
</dl>

<dl>
<dd>

**auto_truncate:** `typing.Optional[bool]` 

Controls the behavior of the platform when the text in your request exceeds 2,000 tokens. Requires Marengo 3.5.

**Values**:
- `false`: The platform returns a `400` error.
- `true`: Truncate your text to fit the limit, and set the [`usage.truncated`](/v1.3/api-reference/create-embeddings-v2/create-embeddings#response.body.usage.truncated) field to `true` in the response.
    
</dd>
</dl>

<dl>
<dd>

**embedding_uncertainty:** `typing.Optional[bool]` 

Set this parameter to `true` to include a per-dimension uncertainty vector in the [`data[].embedding_uncertainty`](/v1.3/api-reference/create-embeddings-v2/create-embeddings#response.body.data.embedding-uncertainty) field of the response. The vector has the same length as the `embedding` array. A higher value indicates lower confidence in that dimension. This requires the Marengo 3.5 native input format. With `model_name: marengo3.0`, setting this parameter to `true` returns `400` (`parameter_invalid`). Marengo 3.5 requests using the compatible format do not return uncertainty vectors.

**Requirements**:
- Set this parameter to `true` only for a text-only request or a single image. Combining text with media, supplying multiple media sources, or supplying audio/video returns a `400` error.
- The platform returns a `400` error if your request includes a document, whether PDF, plain text, or Markdown.
    
</dd>
</dl>

<dl>
<dd>

**embedding_dimension:** `typing.Optional[int]` 

The number of dimensions for each embedding in the response, including the [`data[].embedding_uncertainty`](/v1.3/api-reference/create-embeddings-v2/create-embeddings#response.body.data.embedding-uncertainty) vector.

Marengo 3.5 produces Matryoshka embeddings: a shorter embedding consists of the first values of the full-length embedding. A 256-dimension embedding, for example, is the first 256 values of a 512-dimension embedding of the same content. Shorter embeddings reduce index size and speed up similarity search; longer embeddings produce higher retrieval quality.

**Requirements**:
- This field requires the Marengo 3.5 native input format. An explicit value returns `400` (`parameter_invalid`) with Marengo 3.0 or Marengo 3.5 requests using the compatible input format. Those paths omit dimension metadata when this field is omitted.
- Applies to the entire request: you cannot set it for a single input type or embedding.
- Use the same value across an index.

**Default**: 512
    
</dd>
</dl>

<dl>
<dd>

**text:** `typing.Optional[TextInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**image:** `typing.Optional[ImageInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**text_image:** `typing.Optional[TextImageInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**audio:** `typing.Optional[AudioInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**video:** `typing.Optional[VideoInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**multi_input:** `typing.Optional[MultiInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Embed V2 Tasks
<details><summary><code>client.embed.v_2.tasks.<a href="src/twelvelabs/embed/v_2/tasks/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of the async embedding tasks in your account, including tasks created as part of a batch. The platform returns tasks sorted by creation date, with the newest at the top of the list. The `custom_id` field of a task created as part of a batch is unique only within one batch, identified by the `batch_id` field.

<Note title="Notes">
- Embeddings of a task that is not part of a batch are available through the API for seven days. Tasks created as part of a batch, and their results, are available for up to 30 days from batch creation. Deleting a batch with a final status ends API access to its tasks and results earlier.
- Without the `started_at` or `ended_at` query parameters, this method lists tasks created in the last seven days. Supplying the `batch_id` query parameter removes that default seven-day time window so all retained tasks created as part of that batch can be listed. Explicit time filters still apply. There is no filter that limits the list to tasks that are not part of a batch; without the `batch_id` query parameter, the list can include tasks created as part of a batch.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.embed.v_2.tasks.list(
    started_at="2024-03-01T00:00:00Z",
    ended_at="2024-03-01T00:00:00Z",
    status="queued",
    client_task_id="video_001",
    batch_id="68d3ae81c4a8d3697e15b2ef",
    page=1,
    page_limit=1,
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**started_at:** `typing.Optional[str]` — Retrieve the embedding tasks that were created at or after the given date and time, expressed in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ").
    
</dd>
</dl>

<dl>
<dd>

**ended_at:** `typing.Optional[str]` — Retrieve the embedding tasks that were created at or before the given date and time, expressed in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ").
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[TasksListRequestStatus]` — Filter async embedding tasks by their current status.
    
</dd>
</dl>

<dl>
<dd>

**client_task_id:** `typing.Optional[ClientEmbeddingTaskId]` — Filter tasks that are not part of a batch by the identifier you set when you created the task. The match is exact, and the identifier is unique within your account. A missing task returns an empty `data` array. This filter combines with other list filters using AND and is applied before pagination. The `page_info` counts describe the filtered result set.
    
</dd>
</dl>

<dl>
<dd>

**batch_id:** `typing.Optional[str]` — Filter tasks by the batch they were created in. This filter is applied before pagination and combines with other filters using AND. Without the `started_at` or `ended_at` query parameters, it lists all retained tasks created as part of the batch instead of applying the default seven-day list window. Tasks created as part of the batch are available for up to 30 days from batch creation. Deleting a batch with a final status ends API access to its tasks and results earlier.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` — A number that identifies the page to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` — The number of items to return on each page.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.v_2.tasks.<a href="src/twelvelabs/embed/v_2/tasks/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method creates embeddings for audio, video, images, and documents asynchronously.

Use this method to embed content at scale, such as long files or the media files you want to make searchable. For a query, or for results you need in the same request, use the [`POST`](/v1.3/api-reference/create-embeddings-v2/create-embeddings) method of the `/embed-v2` endpoint instead.

Set the `client_task_id` field to find the task if the request times out or returns a `500` or `503` error. Without it, a retry can create a second task. Reusing an identifier while the original task exists returns `409` and does not create another task. When you supply it, the platform returns the identifier unchanged in the creation response and in later task reads and lists.

When the platform admits a Marengo 3.5 request under a service tier, omitting the `service_tier` field selects Standard. This applies whether or not you set the `client_task_id` field. Those creation, retrieval, and list responses return the applied tier.

The status in the `202` response depends on the creation path. A Marengo 3.5 task admitted under a service tier returns `queued`, including a default Standard task that omits both `service_tier` and `client_task_id`, or `failed` if source validation fails during admission. A Marengo 3.0 task, or a Marengo 3.5 task created on the legacy path, returns `processing`. The same request can return `queued` in place of `processing` when default Standard admission becomes available. A `queued` task has no final status yet. Poll until the status is `ready`, `failed`, or `canceled`.

Because the status in the creation response varies, handle all five statuses when you poll: `queued`, `processing`, `ready`, `failed`, and `canceled`.

With Marengo 3.5, set the `service_tier` field to one of these values: `standard`, `priority`, or `flex`. When the platform processes queued tasks, Priority tasks are preferred over Standard tasks, and Flex tasks use otherwise unused capacity. Tiers are best effort. They do not guarantee a start time, a completion time, or the order in which tasks start or finish, and they do not preempt running tasks. They do not bypass the rate limits or the account capacity for unfinished Flex tasks. The `flex` tier has a 24-hour processing window that starts when the platform accepts the task. The platform returns the `expires_at` field in creation, retrieval, and list responses. An incomplete Flex task becomes `canceled` when that window expires. Availability depends on your plan. Marengo 3.0 does not accept an explicit value for the `service_tier` field.

The content this method accepts depends on the model. Both models embed audio and video. Marengo 3.5 also embeds images and documents: PDF, plain text, and Markdown files. For the formats, resolutions, file sizes, and duration limits each model accepts, see the input requirements for [Marengo 3.5](/v1.3/docs/concepts/models/marengo/marengo-3-5#input-requirements) or [Marengo 3.0](/v1.3/docs/concepts/models/marengo/marengo-3-0#input-requirements).

Creating embeddings asynchronously requires three steps:

1. Create a task using this method. The platform returns a task identifier.
2. Poll for the status of the task using the [`GET`](/v1.3/api-reference/create-embeddings-v2/retrieve-embeddings) method of the `/embed-v2/tasks/{task_id}` endpoint. Stop when the status is `ready`, `failed`, or `canceled`.
3. When the status is `ready`, read the embeddings from that response.

<Note title="Notes">
- For audio or video URL tasks admitted under a service tier, creation checks for an absolute HTTP(S) URL with a hostname and no embedded credentials. An invalid URL returns `400` without creating a task. The platform then downloads the file through public-address and redirect checks and validates the media after acceptance. A task can fail with `SOURCE_INVALID`, `SOURCE_UNAVAILABLE`, or `PAYLOAD_TOO_LARGE` when these checks fail.
- Creation does not validate the full content of a source. For a task admitted under a service tier, the platform checks audio and video URL content and duration after it accepts the task, so the task can fail later. The legacy path checks audio and video media before it accepts a task and can reject the request with `400`. This distinction also applies when a Marengo 3.5 request omits both `service_tier` and `client_task_id`: default Standard admission uses the first path when available, while legacy creation uses the second. When you retrieve an accepted task, check the [`status`](/v1.3/api-reference/create-embeddings-v2/retrieve-embeddings#response.body.status) field. If it is `failed`, the [`error.message`](/v1.3/api-reference/create-embeddings-v2/retrieve-embeddings#response.body.error.message) field contains the reason.
- This method is rate-limited. With Marengo 3.5, the platform counts input tokens for each type of content. A task can exceed a limit before you see an error. For details, see [Input token limits for embedding](/v1.3/docs/get-started/plans-and-billing/rate-limits/new-billing#input-token-limits-for-embedding).
- Embeddings of a task that is not part of a batch are available through the API for seven days. Tasks created as part of a batch, and their results, are available for up to 30 days from batch creation. Deleting a batch with a final status ends API access to its tasks and results earlier.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import AsyncAudioInputRequest, MediaSource, TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.v_2.tasks.create(
    input_type="audio",
    model_name="marengo3.5",
    audio=AsyncAudioInputRequest(
        media_source=MediaSource(
            url="https://user-bucket.com/audio/long-audio.wav",
        ),
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**input_type:** `CreateAsyncEmbeddingRequestInputType` 

The type of content for the embeddings.

**Values**:
- `audio`: An audio file.
- `video`: A video file.
- `document`: A PDF, plain text, or Markdown file. Requires Marengo 3.5.
- `image`: An image file. Requires Marengo 3.5.
    
</dd>
</dl>

<dl>
<dd>

**model_name:** `CreateAsyncEmbeddingRequestModelName` 

The embedding model to use.

**Values**:
- `marengo3.5`: For details about this version, see the [Marengo 3.5](/v1.3/docs/concepts/models/marengo/marengo-3-5) page.
- `marengo3.0`: For details about this version, see the [Marengo 3.0](/v1.3/docs/concepts/models/marengo/marengo-3-0) page.
    
</dd>
</dl>

<dl>
<dd>

**embedding_uncertainty:** `typing.Optional[bool]` 

Set this parameter to `true` to include a per-dimension uncertainty vector in the [`data[].embedding_uncertainty`](/v1.3/api-reference/create-embeddings-v2/retrieve-embeddings#response.body.data.embedding-uncertainty) field of the result. The vector has the same length as the `embedding` array. A higher value indicates lower confidence in that dimension. This requires the Marengo 3.5 native input format. With `model_name: marengo3.0`, setting this parameter to `true` returns `400` (`parameter_invalid`). Marengo 3.5 requests using the compatible format do not return uncertainty vectors.

**Requirements**:
- For audio or video input, set the `embedding_scope` field to exclude `asset`. For example, set the `video.embedding_scope` field to `["clip"]`. The field defaults to `["clip", "asset"]`, so the platform returns a `400` error if you keep the default. This requirement does not apply to image input.
- For a PDF document, the platform returns a `400` error regardless of the `document.embedding_scope` value.
- For a plain text or Markdown document, set the `document.embedding_scope` field to `["local"]`. Any other value returns a `400` error.
    
</dd>
</dl>

<dl>
<dd>

**embedding_dimension:** `typing.Optional[int]` 

The number of dimensions for each embedding that the task produces, including the [`data[].embedding_uncertainty`](/v1.3/api-reference/create-embeddings-v2/retrieve-embeddings#response.body.data.embedding-uncertainty) vector.

Marengo 3.5 produces Matryoshka embeddings: a shorter embedding consists of the first values of the full-length embedding. A 256-dimension embedding, for example, is the first 256 values of a 512-dimension embedding of the same content. Shorter embeddings reduce index size and speed up similarity search; longer embeddings produce higher retrieval quality.

**Requirements**:
- This field requires the Marengo 3.5 native input format. An explicit value returns `400` (`parameter_invalid`) with Marengo 3.0 or Marengo 3.5 requests using the compatible input format. Those paths omit dimension metadata when this field is omitted.
- Applies to the entire task: you cannot set it for a single input type or embedding.
- For audio or video input, fused embeddings with the `asset` scope require `512`. This applies whenever the `embedding_type` field includes the `fused_embedding` value and the `embedding_scope` field includes the `asset` value, even if the task also requests separate embeddings or the `clip` or `local` scope. A task requesting this combination at `128` or `256` fails with the `UNSUPPORTED_COMBINATION` error code; it does not return only the supported outputs.
- Set it once, when you create the task. To use a different value, create a new task.
- Use the same value across an index.

**Default**: 512
    
</dd>
</dl>

<dl>
<dd>

**service_tier:** `typing.Optional[EmbeddingServiceTier]` 
    
</dd>
</dl>

<dl>
<dd>

**client_task_id:** `typing.Optional[ClientEmbeddingTaskId]` 
    
</dd>
</dl>

<dl>
<dd>

**audio:** `typing.Optional[AsyncAudioInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**video:** `typing.Optional[AsyncVideoInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**document:** `typing.Optional[AsyncDocumentInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**image:** `typing.Optional[AsyncImageInputRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.v_2.tasks.<a href="src/twelvelabs/embed/v_2/tasks/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves the status and the results of an async embedding task.

Invoke this method repeatedly until the `status` field is `ready`, `failed`, or `canceled`. When the status is `ready`, use the embeddings from the response. When the status is `failed`, the `error.message` field contains the reason. A canceled task has the `data` field set to `null` and no `error` field. For Marengo 3.5 Flex tasks, the `expires_at` field marks the end of the 24-hour processing window; a task still incomplete then becomes `canceled` with the `deadline_exceeded` value in the `cancellation_reason` field. Work already running can continue, but a late result does not replace the final status or produce successful-task billing.

<Note title="Note">
Embeddings of a task that is not part of a batch are available through the API for seven days. A task created as part of a batch, and its results, are available for up to 30 days from batch creation. Deleting a batch with a final status ends API access to its tasks and results earlier. A task created as part of a batch returns the `batch_id` field and a `custom_id` field that is unique only within the batch.

A task that is not part of a batch can report the `ready` status and later report the `failed` status with the `RESULT_EXPIRED` code, even though the retention period has not ended. This applies to some tasks that have no `service_tier` field, and the later response can contain only the `message` field. After the retention period, retrieval returns `404`. To generate the embeddings again, submit the original input in a new request. Retrieving the same result again does not regenerate it.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.v_2.tasks.retrieve(
    task_id="64f8d2c7e4a1b37f8a9c5d12",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**task_id:** `str` — The unique identifier of the embedding task.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.v_2.tasks.<a href="src/twelvelabs/embed/v_2/tasks/client.py">cancel</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method cancels a task that is not part of a batch in your account while the task is `queued` or `processing`. The task then reports `canceled` with `cancellation_reason: user_requested` and has no embeddings. If you cancel a task that is already canceled, the platform returns `200` with the original cancellation reason. The platform returns `409` if the task is `ready` or `failed`, was created as part of a batch, or has no `service_tier` field. For a batch, use the `POST` method of the `/embed-v2/batches/{batch_id}/cancel` endpoint. If the platform returns `task_cancel_not_supported`, continue to poll the task. Work that is already running can continue after cancellation, but the platform does not return or bill its late result.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.v_2.tasks.cancel(
    task_id="64f8d2c7e4a1b37f8a9c5d12",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**task_id:** `str` — The unique identifier of the embedding task.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Embed V2 Batches
<details><summary><code>client.embed.v_2.batches.<a href="src/twelvelabs/embed/v_2/batches/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to list your batches. The response sorts batches by creation date, with the newest batch first. Each batch includes its status and item counts.

**Notes**:
- Filters combine using AND.
- To retrieve the status and the task identifier of each item in a batch, use the [`GET`](/v1.3/api-reference/create-embeddings-v2/batches/retrieve-batch-status) method of the `/embed-v2/batches/{batch_id}` endpoint.
- To retrieve the embeddings of a batch, use the [`GET`](/v1.3/api-reference/create-embeddings-v2/batches/retrieve-batch-results) method of the `/embed-v2/batches/{batch_id}/results` endpoint.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.v_2.batches.list(
    client_batch_id="reports_2026_10",
    status="pending",
    page=1,
    page_limit=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**client_batch_id:** `typing.Optional[ClientEmbeddingBatchId]` — Filter batches by the identifier you set when you created the batch. The match is exact.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[BatchesListRequestStatus]` — Filter batches by status. For the meaning of each value, see the [Batch statuses](/v1.3/api-reference/create-embeddings-v2/batches/the-batch-object#batch-statuses) section on the **The batch object** page. If you omit this parameter, the response includes batches in all statuses.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve, after the filters are applied.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of batches to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.v_2.batches.<a href="src/twelvelabs/embed/v_2/batches/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to create multiple embeddings in a single call. Each item creates an embedding task. Requires Marengo 3.5.

**When to use this method**:
- Embed multiple items with the same settings. All items in a batch have the same input type: `audio`, `video`, `document`, or `image`. To embed more than one input type, create one batch for each type.
- Track one batch instead of multiple tasks.

**Do not use this method for**:
- Results you need by a set time. Batch items use the Flex service tier. The platform starts them with capacity that other tasks do not use, and it does not guarantee a start time or a completion time. Create a separate task for each item with the [`POST`](/v1.3/api-reference/create-embeddings-v2/create-async-embedding-task) method of the `/embed-v2/tasks` endpoint instead. To use a tier other than Flex, set the `service_tier` field to the `standard` or `priority` value.
- One item. Use the [`POST`](/v1.3/api-reference/create-embeddings-v2/create-async-embedding-task) method of the `/embed-v2/tasks` endpoint instead.
- Results in the same request. Use the [`POST`](/v1.3/api-reference/create-embeddings-v2/create-embeddings) method of the `/embed-v2` endpoint for synchronous embedding instead.

**Validation**:
- An invalid request returns `400` and creates no batch or task.
- A source failure found while the platform accepts the batch fails that item's task. The rest of the batch continues.
- After the platform accepts the batch, it checks the file at each video or audio URL, the duration of the media, and the number of pages in each PDF. If an item fails one of these checks, its task has the `failed` status.

**Retention**:
- The processing window is 24 hours from creation. If it ends while items are unfinished, the batch has the `expired` status, and the platform cancels those items.
- Batches, tasks, and results are available through the API for up to 30 days after creation. Deleting a batch with a final status ends access to its tasks and results earlier.
- Only ready items are billed.

**Limits**:
- A batch contains 1 to 1,000 items.
- For the formats, resolutions, file sizes, and duration limits of each item, see the input requirements for [Marengo 3.5](/v1.3/docs/concepts/models/marengo/marengo-3-5#input-requirements).
- The configured request body limit covers the entire JSON body, including base64 media. It is separate from the size limit of each media file. If the API rejects a body with `413`, its error message reports the configured limit in bytes. Use a URL or supported `asset_id` for media that does not fit.
- A limit applies to the number of Flex tasks that are `queued` or `processing` at the same time, including the tasks of a batch. A request that exceeds the limit returns `429`.
- When a request-count limit applies, each request to create a batch counts once, regardless of the number of items it contains. The limit is shared with requests that create a task that is not part of a batch. A request that fails before the platform accepts the batch does not count.
- Input-token limits count the usage of completed work, and the platform does not reserve the tokens of a batch when you create it. Items already accepted can finish and take usage above a limit, and a later create request can then return `429`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import (
    EmbeddingBatchDefaultsRequest,
    EmbeddingBatchVideoDefaultsRequest,
    EmbeddingBatchVideoInputRequest,
    EmbeddingBatchVideoItemRequest,
    MediaSource,
    TwelveLabs,
)

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.v_2.batches.create(
    model_name="marengo3.5",
    service_tier="flex",
    input_type="video",
    defaults=EmbeddingBatchDefaultsRequest(
        video=EmbeddingBatchVideoDefaultsRequest(
            embedding_option=["visual", "audio"],
        ),
    ),
    requests=[
        EmbeddingBatchVideoItemRequest(
            custom_id="clip_001",
            video=EmbeddingBatchVideoInputRequest(
                media_source=MediaSource(
                    url="https://example.com/clip.mp4",
                ),
            ),
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_name:** `CreateEmbeddingBatchRequestModelName` — The embedding model to use for every item in this batch.
    
</dd>
</dl>

<dl>
<dd>

**service_tier:** `CreateEmbeddingBatchRequestServiceTier` 

The [service tier](/v1.3/docs/advanced/service-tiers) for every item in this batch.

**Values**:
- `flex`: Uses capacity that other tasks do not use. Processing ends 24 hours after the platform accepts the task. The platform cancels a task that is not complete by then.

Use the `standard` and `priority` values only for a task that is not part of a batch.
    
</dd>
</dl>

<dl>
<dd>

**input_type:** `CreateEmbeddingBatchRequestInputType` — The input type for every item in this batch.
    
</dd>
</dl>

<dl>
<dd>

**requests:** `typing.Sequence[EmbeddingBatchItemRequest]` — The embedding requests in the batch. Provide 1 to 1,000 requests. In each request, set only the field that matches the `input_type` field: `audio`, `video`, `document`, or `image`.
    
</dd>
</dl>

<dl>
<dd>

**client_batch_id:** `typing.Optional[ClientEmbeddingBatchId]` 
    
</dd>
</dl>

<dl>
<dd>

**defaults:** `typing.Optional[EmbeddingBatchDefaultsRequest]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.v_2.batches.<a href="src/twelvelabs/embed/v_2/batches/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to monitor a batch. The response includes the batch status, the item counts, and one entry for each item with its `custom_id` value and task identifier.

Poll this method until the batch reaches the `completed`, `canceled`, or `expired` status. To retrieve the embeddings, use the [`GET`](/v1.3/api-reference/create-embeddings-v2/batches/retrieve-batch-results) method of the `/embed-v2/batches/{batch_id}/results` endpoint.

Do not treat the `completed` status as a success signal. It means that every item reached a final status, not that every embedding succeeded. To see how many items succeeded, failed, or were canceled, check the `ready_items`, `failed_items`, and `canceled_items` fields.

The platform keeps a batch and its tasks readable for 30 days after batch creation, regardless of their statuses. After that period, reads of the batch, its results, and its tasks return `404`. Deletion ends access earlier.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.v_2.batches.retrieve(
    batch_id="68d3ae81c4a8d3697e15b2ef",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**batch_id:** `str` — The unique identifier of the batch.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.v_2.batches.<a href="src/twelvelabs/embed/v_2/batches/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to delete a batch. After you delete a batch, you can no longer retrieve the batch, its tasks, or its results. You can only delete batches with the `completed`, `canceled`, or `expired` status.

Deleting a batch does not affect billing. You are billed for every item that completed successfully, regardless of whether you delete the batch afterward.

To stop a batch with the `pending` or `processing` status, use the [`POST`](/v1.3/api-reference/create-embeddings-v2/batches/cancel-batch) method of the `/embed-v2/batches/{batch_id}/cancel` endpoint, and wait for the batch to reach a final status.

Batches and their results are available through the API for 30 days after creation.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.v_2.batches.delete(
    batch_id="68d3ae81c4a8d3697e15b2ef",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**batch_id:** `str` — The unique identifier of the batch.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.v_2.batches.<a href="src/twelvelabs/embed/v_2/batches/client.py">results</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to retrieve the results for each item in a batch. You can call it while the batch has the `pending` or `processing` status.

The response is a JSON Lines stream. Each line is a result entry, and there is one result entry for each item. Each result entry has a status. For details on each status, see the [Item statuses](/v1.3/api-reference/create-embeddings-v2/batches/the-batch-object#item-statuses) section on the **The batch object** page.

You can retrieve results for 30 days after batch creation.

**Notes**:
- Result entries are not guaranteed to appear in submission order.
- A `200` status does not confirm a complete stream. To verify it, count the distinct `custom_id` values and compare the count with the `total_items` field of the batch. If the connection ends early, retry and verify the count again.
- If an error occurs after the stream starts, the response ends early and the platform sends the `X-Stream-Error` trailer. A trailer is an HTTP header that the platform sends after the response body. The trailer contains the `stream_error` code. Many HTTP clients do not show trailers, so always compare the number of result entries with the `total_items` field.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.embed.v_2.batches.results(
    batch_id="68d3ae81c4a8d3697e15b2ef",
)
for chunk in response:
    print(chunk)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**batch_id:** `str` — The unique identifier of the batch.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.embed.v_2.batches.<a href="src/twelvelabs/embed/v_2/batches/client.py">cancel</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Use this method to request cancellation of a batch that has the `pending` or `processing` status.

When you invoke this method, the platform performs the following steps:
- Cancels the items in the `queued` status.
- Finishes processing the items in the `processing` status. Each reaches its own final result.

The batch has the `canceling` status until those items finish, then the `canceled` status. If a running item does not finish before the time in the `expires_at` field of the batch, the platform cancels it with the `deadline_exceeded` reason, and the batch has the `expired` status.

**Billing and results**:
- An item that is processing when you cancel can still become `ready`. You are billed for it, and its result is available with the results that were ready before the cancellation.
- An item that finishes after the time in the `expires_at` field of the batch stays canceled and is not billed.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.embed.v_2.batches.cancel(
    batch_id="68d3ae81c4a8d3697e15b2ef",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**batch_id:** `str` — The unique identifier of the batch.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EntityCollections Entities
<details><summary><code>client.entity_collections.entities.<a href="src/twelvelabs/entity_collections/entities/client.py">list_by_asset</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of entities whose [`asset_ids`](/v1.3/api-reference/entities/entity-collections/entities/retrieve#response.body.asset_ids) array contains the specified asset.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.entity_collections.entities.list_by_asset(
    asset_id="6298d673f1090f1100476d4c",
    page=1,
    page_limit=10,
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.entities.<a href="src/twelvelabs/entity_collections/entities/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of the entities in the specified entity collection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.entity_collections.entities.list(
    entity_collection_id="6298d673f1090f1100476d4c",
    page=1,
    page_limit=10,
    name="My entity",
    status="processing",
    sort_by="created_at",
    sort_option="desc",
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection for which the platform will retrieve the entities.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — Filter entities by name.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[EntitiesListRequestStatus]` — Filter entities by status.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[EntitiesListRequestSortBy]` 

The field to sort on. The following options are available:
- `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the entity was created.
- `updated_at:` Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the entity collection was updated.
- `name`: Sorts by the name.
    
</dd>
</dl>

<dl>
<dd>

**sort_option:** `typing.Optional[str]` 

The sorting direction. The following options are available:
- `asc`
- `desc`

**Default**: `desc`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.entities.<a href="src/twelvelabs/entity_collections/entities/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method creates an entity within a specified entity collection. Each entity must be associated with at least one asset.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.entities.create(
    entity_collection_id="6298d673f1090f1100476d4c",
    name="My entity",
    asset_ids=["6298d673f1090f1100476d4c", "6298d673f1090f1100476d4d"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection in which to create the entity.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the entity. Make sure you use a succinct and descriptive name.
    
</dd>
</dl>

<dl>
<dd>

**asset_ids:** `typing.Sequence[str]` — An array of asset IDs to associate with the entity. You must provide at least one value.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An optional description of the entity.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` 

Optional metadata for the entity, provided as key-value pairs to store additional context or attributes. Use metadata to categorize or describe the entity for easier management and search. Keys must be of type `string`, and values can be of type `string`, `integer`, `float`, or `boolean`.

**Example**:
```json
{
  "sport": "soccer",
  "teamId": 42,
  "performanceScore": 8.7,
  "isActive": true
}
```

<Note title="Note">
  To store complex data types such as objects or arrays, convert them to string values before including them in the metadata.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.entities.<a href="src/twelvelabs/entity_collections/entities/client.py">create_bulk</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method creates multiple entities within a specified entity collection in a single request. Each entity must be associated with at least one asset. This endpoint is useful for efficiently adding multiple entities, such as a roster of players or a group of characters.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs
from twelvelabs.entity_collections.entities import (
    EntitiesCreateBulkRequestEntitiesItem,
)

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.entities.create_bulk(
    entity_collection_id="6298d673f1090f1100476d4c",
    entities=[
        EntitiesCreateBulkRequestEntitiesItem(
            name="My entity",
            asset_ids=["6298d673f1090f1100476d4c", "6298d673f1090f1100476d4d"],
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection in which to create the entities.
    
</dd>
</dl>

<dl>
<dd>

**entities:** `typing.Sequence[EntitiesCreateBulkRequestEntitiesItem]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.entities.<a href="src/twelvelabs/entity_collections/entities/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves details about the specified entity.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.entities.retrieve(
    entity_collection_id="6298d673f1090f1100476d4c",
    entity_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection.
    
</dd>
</dl>

<dl>
<dd>

**entity_id:** `str` — The unique identifier of the entity to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.entities.<a href="src/twelvelabs/entity_collections/entities/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes a specific entity from an entity collection. It permanently removes the entity and its associated data, but does not affect the assets associated with this entity.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.entities.delete(
    entity_collection_id="6298d673f1090f1100476d4c",
    entity_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection containing the entity to be deleted.
    
</dd>
</dl>

<dl>
<dd>

**entity_id:** `str` — The unique identifier of the entity to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.entities.<a href="src/twelvelabs/entity_collections/entities/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method updates the specified entity within an entity collection. This operation allows modification of the entity's name, description, or metadata. Note that this endpoint does not affect the assets associated with the entity.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.entities.update(
    entity_collection_id="6298d673f1090f1100476d4c",
    entity_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection containing the entity to be updated.
    
</dd>
</dl>

<dl>
<dd>

**entity_id:** `str` — The unique identifier of the entity to update.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The new name for the entity.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An updated description for the entity.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` — Updated metadata for the entity. If provided, this completely replaces the existing metadata. Use this to store custom key-value pairs related to the entity.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.entities.<a href="src/twelvelabs/entity_collections/entities/client.py">create_assets</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method adds assets to the specified entity within an entity collection. Assets are used to identify the entity in media content, and adding multiple assets can improve the accuracy of entity recognition in searches.

When assets are added, the entity may temporarily enter the "processing" state while the platform updates the necessary data. Once processing is complete, the entity status will return to "ready."
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.entities.create_assets(
    entity_collection_id="6298d673f1090f1100476d4c",
    entity_id="6298d673f1090f1100476d4c",
    asset_ids=["6298d673f1090f1100476d4c", "6298d673f1090f1100476d4d"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection that contains the entity to which assets will be added.
    
</dd>
</dl>

<dl>
<dd>

**entity_id:** `str` — The unique identifier of the entity within the specified entity collection to which the assets will be added.
    
</dd>
</dl>

<dl>
<dd>

**asset_ids:** `typing.Sequence[str]` — An array of asset IDs to add to the entity.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entity_collections.entities.<a href="src/twelvelabs/entity_collections/entities/client.py">delete_assets</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method removes from the specified entity. Assets are used to identify the entity in media content, and removing assets may impact the accuracy of entity recognition in searches if too few assets remain.

When assets are removed, the entity may temporarily enter a "processing" state while the system updates the necessary data. Once processing is complete, the entity status will return to "ready."

<Note title="Notes">
  - This operation only removes the association between the entity and the specified assets; it does not delete the assets themselves.
  - An entity must always have at least one asset associated with it. You can't remove the last asset from an entity.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.entity_collections.entities.delete_assets(
    entity_collection_id="6298d673f1090f1100476d4c",
    entity_id="6298d673f1090f1100476d4c",
    asset_ids=["6298d673f1090f1100476d4e", "6298d673f1090f1100476d4f"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_collection_id:** `str` — The unique identifier of the entity collection that contains the entity from which assets will be removed.
    
</dd>
</dl>

<dl>
<dd>

**entity_id:** `str` — The unique identifier of the entity within the specified entity collection from which the assets will be removed.
    
</dd>
</dl>

<dl>
<dd>

**asset_ids:** `typing.Sequence[str]` — An array of asset IDs to remove from the entity.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Indexes IndexedAssets
<details><summary><code>client.indexes.indexed_assets.<a href="src/twelvelabs/indexes/indexed_assets/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of the indexed assets in the specified index. By default, the platform returns your indexed assets sorted by creation date, with the newest at the top of the list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.indexes.indexed_assets.list(
    index_id="6298d673f1090f1100476d4c",
    page=1,
    page_limit=10,
    sort_by="created_at",
    sort_option="desc",
    status=["ready"],
    filename="01.mp4",
    created_at="2024-08-16T16:53:59Z",
    updated_at="2024-08-16T16:53:59Z",
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index for which the platform will retrieve the indexed assets.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[str]` 

The field to sort on. The following options are available:
- `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was updated.
- `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was created.

**Default**: `created_at`.
    
</dd>
</dl>

<dl>
<dd>

**sort_option:** `typing.Optional[str]` 

The sorting direction. The following options are available:
- `asc`
- `desc`

**Default**: `desc`.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[
    typing.Union[
        IndexedAssetsListRequestStatusItem,
        typing.Sequence[IndexedAssetsListRequestStatusItem],
    ]
]` 

Filter by one or more indexing task statuses. The following options are available:
- `ready`: The indexed asset has been successfully uploaded and indexed.
- `pending`: The indexed asset is pending.
- `queued`: The indexed asset is queued.
- `indexing`: The indexed asset is being indexed.
- `validating`: The indexed asset is being validated.
- `failed`: The indexed asset indexing task failed.

To filter by multiple statuses, specify the `status` parameter for each value:
```
status=ready&status=validating
```
    
</dd>
</dl>

<dl>
<dd>

**filename:** `typing.Optional[str]` — Filter by filename.
    
</dd>
</dl>

<dl>
<dd>

**duration:** `typing.Optional[IndexedAssetsListRequestDuration]` 

Filter by duration in seconds. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**fps:** `typing.Optional[IndexedAssetsListRequestFps]` 

Filter by frames per second. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**width:** `typing.Optional[IndexedAssetsListRequestWidth]` 

Filter by width in pixels. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**height:** `typing.Optional[IndexedAssetsListRequestHeight]` 

Filter by height in pixels. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**size:** `typing.Optional[IndexedAssetsListRequestSize]` 

Filter by size in bytes. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**created_at:** `typing.Optional[str]` — Filter indexed assets by the creation date and time of their associated indexing tasks, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns indexed assets created on or after the specified date and time.
    
</dd>
</dl>

<dl>
<dd>

**updated_at:** `typing.Optional[str]` — This filter applies only to indexed assets updated using the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/{index-id}/indexed-assets/{indexed-asset-id}` endpoint. It filters indexed assets by the last update date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the indexed assets that were last updated on the specified date at or after the given time.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `typing.Optional[
    typing.Dict[str, typing.Optional[IndexedAssetsListRequestUserMetadataValue]]
]` 

To enable filtering by custom fields, you must first add user-defined metadata to your video by calling the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/:index-id/indexed-assets/:indexed-asset-id` endpoint.

Examples:
- To filter on a string: `?category=recentlyAdded`
- To filter on an integer: `?batchNumber=5`
- To filter on a float: `?rating=9.3`
- To filter on a boolean: `?needsReview=true`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.indexed_assets.<a href="src/twelvelabs/indexes/indexed_assets/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method indexes an uploaded asset to make it searchable and analyzable. Indexing processes your content and extracts information that enables the platform to search and analyze your videos.

This operation is asynchronous. The platform returns an indexed asset ID immediately and processes your content in the background. Monitor the indexing status to know when your content is ready to use.

<Note title="Adding videos to existing indexes">
You can no longer add videos to an index that has only Pegasus 1.2 enabled. When you add videos to an index that has both Marengo and Pegasus 1.2 enabled, the platform indexes them with Marengo only.
</Note>

Your asset must meet the requirements based on your workflow:
- **Search**: [Marengo requirements](/v1.3/docs/concepts/models/marengo/marengo-3-0#video-file-requirements)
- **Video analysis**: [Pegasus requirements](/v1.3/docs/concepts/models/pegasus/pegasus-1-6#input-requirements).

If you want to both search and analyze your videos, the most restrictive requirements apply.

Indexes have limits on video hours and video count. For details, see the [Video hours and video count limits](/v1.3/docs/concepts/indexes#video-hours-and-video-count-limits) section.

<Note title="Note">
This endpoint is rate-limited. For details, see the [Rate limits](/v1.3/docs/get-started/rate-limits) page.
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.indexed_assets.create(
    index_id="6298d673f1090f1100476d4c",
    asset_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index to which the asset will be indexed.
    
</dd>
</dl>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset to index. The asset status must be `ready`. Use the [Retrieve an asset](/v1.3/api-reference/upload-content/direct-uploads/retrieve) method to check the status. If you uploaded the asset before your plan moved to the new billing, enable storage accounting for it before you index it in an index for which Marengo is enabled. Use the [Enable storage accounting for an asset](/v1.3/api-reference/manage-assets/enable-storage-accounting) method.
    
</dd>
</dl>

<dl>
<dd>

**enable_video_stream:** `typing.Optional[bool]` — This parameter indicates if the platform stores the video for streaming. When set to `true`, the platform stores the video, and you can retrieve its URL by calling the [`GET`](/v1.3/api-reference/videos/retrieve) method of the `/indexes/{index-id}/indexed-assets/{indexed-asset-id}` endpoint. You can then use this URL to access the stream over the <a href="https://en.wikipedia.org/wiki/HTTP_Live_Streaming" target="_blank">HLS</a> protocol.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `typing.Optional[UserMetadata]` — Metadata that helps you categorize your assets. You can specify a list of keys and values. Keys are strings, and values can be a string, a number, a boolean, or an array of strings. A key set to an empty string (`""`), an empty array (`[]`), or `null` is omitted. Send an integer wider than 53 bits (-9007199254740991 to 9007199254740991), and any identifier you want preserved verbatim, as a string.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.indexed_assets.<a href="src/twelvelabs/indexes/indexed_assets/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method retrieves information about an indexed asset, including its status, metadata, and optional embeddings or transcription.

Use this method to:

- Monitor the indexing progress:
    - Call this endpoint after creating an indexed asset
    - Check the `status` field until it shows `ready`
    - Once ready, your content is available for search and analysis

- Retrieve the asset metadata:
    - Retrieve system metadata (duration, resolution, filename)
    - Access user-defined metadata

- Retrieve the embeddings:
    - Include the `embeddingOption` parameter to retrieve video embeddings
    - Requires the Marengo video understanding model to be enabled in your index

- Retrieve transcriptions:
  - Set the `transcription` parameter to `true` to retrieve spoken words from your video
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.indexed_assets.retrieve(
    index_id="6298d673f1090f1100476d4c",
    indexed_asset_id="6298d673f1090f1100476d4c",
    embedding_option=["visual"],
    transcription=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index to which the indexed asset has been uploaded.
    
</dd>
</dl>

<dl>
<dd>

**indexed_asset_id:** `str` — The unique identifier of the indexed asset to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**embedding_option:** `typing.Optional[
    typing.Union[
        IndexedAssetsRetrieveRequestEmbeddingOptionItem,
        typing.Sequence[IndexedAssetsRetrieveRequestEmbeddingOptionItem],
    ]
]` 

Specifies which types of embeddings to retrieve. Values: `visual`, `audio`, `transcription`. For details, see the [Embedding options](/v1.3/docs/concepts/modalities#embedding-options) section.

<Note title="Note">
To retrieve embeddings for a video, it must be indexed using the Marengo video understanding model. For details on enabling this model for an index, see the [Create an index](/reference/create-index) page.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**transcription:** `typing.Optional[bool]` — Specifies whether to retrieve a transcription of the spoken words.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.indexed_assets.<a href="src/twelvelabs/indexes/indexed_assets/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method deletes all the information about the specified indexed asset. This action cannot be undone.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.indexed_assets.delete(
    index_id="6298d673f1090f1100476d4c",
    indexed_asset_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index to which the indexed asset has been uploaded.
    
</dd>
</dl>

<dl>
<dd>

**indexed_asset_id:** `str` — The unique identifier of the indexed asset to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.indexed_assets.<a href="src/twelvelabs/indexes/indexed_assets/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method updates one or more fields of the metadata of an indexed asset. Also, can delete a field by setting it to `null`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.indexed_assets.update(
    index_id="6298d673f1090f1100476d4c",
    indexed_asset_id="6298d673f1090f1100476d4c",
    user_metadata={
        "category": "recentlyAdded",
        "batchNumber": 5,
        "rating": 9.3,
        "needsReview": True,
        "hashtags": ["summer", "vlog"],
    },
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index to which the indexed asset has been uploaded.
    
</dd>
</dl>

<dl>
<dd>

**indexed_asset_id:** `str` — The unique identifier of the indexed asset to update.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `typing.Optional[UserMetadata]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.indexed_assets.<a href="src/twelvelabs/indexes/indexed_assets/client.py">list_by_asset</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This method returns a list of indexed assets that reference the specified asset. Each entry includes the indexed asset ID and the index it belongs to.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.indexes.indexed_assets.list_by_asset(
    asset_id="6298d673f1090f1100476d4c",
    page=1,
    page_limit=10,
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**asset_id:** `str` — The unique identifier of the asset.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Indexes Videos
<details><summary><code>client.indexes.videos.<a href="src/twelvelabs/indexes/videos/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Info>This method will be deprecated in a future version. New implementations should use the [List indexed assets](/v1.3/api-reference/index-content/list) method.</Info>

This method returns a list of the videos in the specified index. By default, the platform returns your videos sorted by creation date, with the newest at the top of the list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
response = client.indexes.videos.list(
    index_id="6298d673f1090f1100476d4c",
    page=1,
    page_limit=10,
    sort_by="created_at",
    sort_option="desc",
    filename="01.mp4",
    created_at="2024-08-16T16:53:59Z",
    updated_at="2024-08-16T16:53:59Z",
)
for item in response:
    print(item)
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    print(page)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index for which the platform will retrieve the videos.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 

A number that identifies the page to retrieve.

**Default**: `1`.
    
</dd>
</dl>

<dl>
<dd>

**page_limit:** `typing.Optional[int]` 

The number of items to return on each page.

**Default**: `10`.
**Max**: `50`.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[str]` 

The field to sort on. The following options are available:
- `updated_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was updated.
- `created_at`: Sorts by the time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when the item was created.

**Default**: `created_at`.
    
</dd>
</dl>

<dl>
<dd>

**sort_option:** `typing.Optional[str]` 

The sorting direction. The following options are available:
- `asc`
- `desc`

**Default**: `desc`.
    
</dd>
</dl>

<dl>
<dd>

**filename:** `typing.Optional[str]` — Filter by filename.
    
</dd>
</dl>

<dl>
<dd>

**duration:** `typing.Optional[VideosListRequestDuration]` 

Filter by duration in seconds. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**fps:** `typing.Optional[VideosListRequestFps]` 

Filter by frames per second. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**width:** `typing.Optional[VideosListRequestWidth]` 

Filter by width in pixels. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**height:** `typing.Optional[VideosListRequestHeight]` 

Filter by height in pixels. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**size:** `typing.Optional[VideosListRequestSize]` 

Filter by size in bytes. Pass an object with `gte` and/or `lte` for range filtering.
For exact match, set both to the same value.
    
</dd>
</dl>

<dl>
<dd>

**created_at:** `typing.Optional[str]` — Filter videos by the creation date and time of their associated indexing tasks, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the videos whose indexing tasks were created on the specified date at or after the given time.
    
</dd>
</dl>

<dl>
<dd>

**updated_at:** `typing.Optional[str]` — This filter applies only to videos updated using the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/{index-id}/videos/{video-id}` endpoint. It filters videos by the last update date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"). The platform returns the video indexing tasks that were last updated on the specified date at or after the given time.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `typing.Optional[
    typing.Dict[str, typing.Optional[VideosListRequestUserMetadataValue]]
]` 

To enable filtering by custom fields, you must first add user-defined metadata to your video by calling the [`PUT`](/v1.3/api-reference/videos/update) method of the `/indexes/:index-id/videos/:video-id` endpoint.

Examples:
- To filter on a string: `?category=recentlyAdded`
- To filter on an integer: `?batchNumber=5`
- To filter on a float: `?rating=9.3`
- To filter on a boolean: `?needsReview=true`
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.videos.<a href="src/twelvelabs/indexes/videos/client.py">retrieve</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Info> This method will be deprecated in a future version. New implementations should use the [Retrieve an indexed asset](/v1.3/api-reference/index-content/retrieve) method.</Info>

This method retrieves information about the specified video.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.videos.retrieve(
    index_id="6298d673f1090f1100476d4c",
    video_id="6298d673f1090f1100476d4c",
    embedding_option=["visual"],
    transcription=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index to which the video has been uploaded.
    
</dd>
</dl>

<dl>
<dd>

**video_id:** `str` — The unique identifier of the video to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**embedding_option:** `typing.Optional[
    typing.Union[
        VideosRetrieveRequestEmbeddingOptionItem,
        typing.Sequence[VideosRetrieveRequestEmbeddingOptionItem],
    ]
]` 

Specifies which types of embeddings to retrieve. Values: `visual`, `audio`, `transcription`. For details, see the [Embedding options](/v1.3/docs/concepts/modalities#embedding-options) section.

<Note title="Note">
To retrieve embeddings for a video, it must be indexed using the Marengo video understanding model. For details on enabling this model for an index, see the [Create an index](/reference/create-index) page.
</Note>
    
</dd>
</dl>

<dl>
<dd>

**transcription:** `typing.Optional[bool]` — The parameter indicates whether to retrieve a transcription of the spoken words for the indexed video.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.videos.<a href="src/twelvelabs/indexes/videos/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Info>This method will be deprecated in a future version. New implementations should use the [Delete an indexed asset](/v1.3/api-reference/index-content/delete) method.</Info>

This method deletes all the information about the specified indexed video. This action cannot be undone.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.videos.delete(
    index_id="6298d673f1090f1100476d4c",
    video_id="6298d673f1090f1100476d4c",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index to which the video has been uploaded.
    
</dd>
</dl>

<dl>
<dd>

**video_id:** `str` — The unique identifier of the video to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.indexes.videos.<a href="src/twelvelabs/indexes/videos/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Info>This method will be deprecated in a future version. New implementations should use the [Partial update indexed asset](/v1.3/api-reference/index-content/update) method.</Info>

This method updates one or more fields of the metadata of a video. Also, can delete a field by setting it to `null`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(
    api_key="YOUR_API_KEY",
)
client.indexes.videos.update(
    index_id="6298d673f1090f1100476d4c",
    video_id="6298d673f1090f1100476d4c",
    user_metadata={
        "category": "recentlyAdded",
        "batchNumber": 5,
        "rating": 9.3,
        "needsReview": True,
        "hashtags": ["summer", "vlog"],
    },
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**index_id:** `str` — The unique identifier of the index to which the video has been uploaded.
    
</dd>
</dl>

<dl>
<dd>

**video_id:** `str` — The unique identifier of the video to update.
    
</dd>
</dl>

<dl>
<dd>

**user_metadata:** `typing.Optional[UserMetadata]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

