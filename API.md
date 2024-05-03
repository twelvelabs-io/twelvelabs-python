## Engine

Methods

- <code>client.engine.retrieve(id) -> Engine</code>
- <code>client.engine.list() -> RootModelList[Engine]</code>

## Index

Methods

- <code>client.index.retrieve(id) -> Index</code>
- <code>client.index.list(\*\*params) -> RootModelList[Index]</code>
- <code>client.index.create(name, engines, \*\*params) -> Index</code>
- <code>client.index.update(id, name) -> None</code>
- <code>client.index.delete(id) -> None</code>

## Tasks

Methods

- <code>client.task.retrieve(id) -> Task</code>
- <code>client.task.list(\*\*params) -> RootModelList[Task]</code>
- <code>client.task.create(index_id, \*\*params) -> Task</code>
- <code>client.task.delete(id) -> None</code>
- <code>client.task.status(index_id) -> TaskStatus</code>
- <code>client.task.transfer(file) -> None</code>
- <code>client.task.external_provider(index_id, url) -> Task</code>

## Video

Methods

- <code>client.video.retrieve(index_id, id) -> Video</code>
- <code>client.video.list(index_id, \*\*params) -> RootModelList[Video]</code>
- <code>client.video.update(index_id, id, \*\*params) -> None</code>
- <code>client.video.delete(index_id, id) -> None</code>
- <code>client.video.transcription(index_id, id, \*\*params) -> RootModelList[VideoValue]</code>
- <code>client.video.text_in_video(index_id, id, \*\*params) -> RootModelList[VideoValue]</code>
- <code>client.video.logo(index_id, id, \*\*params) -> RootModelList[VideoValue]</code>
- <code>client.video.thumbnail(index_id, id, \*\*params) -> str</code>

## Search

Methods

- <code>client.search.query(index_id, query, options, \*\*params) -> SearchResult</code>
- <code>client.search.by_page_token(page_token) -> SearchResult</code>
- <code>client.search.combined_query(index_id, query, options, \*\*params) -> CombinedSearchResult</code>
- <code>client.search.combined_by_page_token(page_token) -> CombinedSearchResult</code>

## Generate

Methods

- <code>client.generate.gist(video_id, types) -> GenerateGistResult</code>
- <code>client.generate.summarize(video_id, type) -> GenerateSummarizeResult</code>
- <code>client.generate.text(video_id, prompt) -> GenerateOpenEndedTextResult</code>
