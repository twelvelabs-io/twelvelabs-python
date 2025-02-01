## Index

Methods

- <code>client.index.retrieve(id) -> Index</code>
- <code>client.index.list(\*\*params) -> RootModelList[Index]</code>
- <code>client.index.create(name, models, \*\*params) -> Index</code>
- <code>client.index.update(id, name) -> None</code>
- <code>client.index.delete(id) -> None</code>

## Task

Methods

- <code>client.task.retrieve(id) -> Task</code>
- <code>client.task.list(\*\*params) -> RootModelList[Task]</code>
- <code>client.task.create(index_id, \*\*params) -> Task</code>
- <code>client.task.delete(id) -> None</code>
- <code>client.task.status(index_id) -> TaskStatus</code>
- <code>client.task.transfers.import_videos(integration_id, index_id, \*\*params) -> TransferImportResponse</code>
- <code>client.task.transfers.import_status(integration_id, index_id) -> TransferImportStatusResponse</code>
- <code>client.task.transfers.import_logs(integration_id) -> RootModelList[TransferImportLog]</code>

## Video

Methods

- <code>client.video.retrieve(index_id, id) -> Video</code>
- <code>client.video.list(index_id, \*\*params) -> RootModelList[Video]</code>
- <code>client.video.update(index_id, id, \*\*params) -> None</code>
- <code>client.video.delete(index_id, id) -> None</code>

## Embed

Methods

- <code>client.embed.create(model_name, \*\*params) -> CreateEmbeddingsResult</code>
- <code>client.embed.task.retrieve(id) -> EmbeddingsTask</code>
- <code>client.embed.task.list(\*\*params) -> RootModelList[EmbeddingsTask]</code>
- <code>client.embed.task.create(model_name, \*\*params) -> EmbeddingsTask</code>
- <code>client.embed.task.status(task_id) -> EmbeddingsTaskStatus</code>

## Search

Methods

- <code>client.search.query(index_id, options, \*\*params) -> SearchResult</code>
- <code>client.search.by_page_token(page_token) -> SearchResult</code>

## Generate

Methods

- <code>client.generate.summarize(video_id, type) -> GenerateSummarizeResult</code>
- <code>client.generate.gist(video_id, types) -> GenerateGistResult</code>
- <code>client.generate.text(video_id, prompt) -> GenerateOpenEndedTextResult</code>
