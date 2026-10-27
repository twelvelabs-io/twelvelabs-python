import contextlib
import json
import typing

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.http_response import AsyncHttpResponse, HttpResponse
from ..core.pydantic_utilities import parse_obj_as
from ..core.request_options import RequestOptions
from ..create_embeddings.client import AsyncCreateEmbeddingsClient, CreateEmbeddingsClient
from ..create_embeddings.raw_client import AsyncRawCreateEmbeddingsClient, RawCreateEmbeddingsClient
from ..types.embedding_batch_result_item import EmbeddingBatchResultItem


def _parse_result(line: str) -> EmbeddingBatchResultItem:
    return parse_obj_as(EmbeddingBatchResultItem, json.loads(line))


class _StrictRawCreateEmbeddingsClient(RawCreateEmbeddingsClient):
    @contextlib.contextmanager
    def retrieve_embedding_batch_results(
        self, batch_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Iterator[HttpResponse[typing.Iterator[EmbeddingBatchResultItem]]]:
        # Keep generated authentication, HTTP errors, and response cleanup, but do
        # not use its decoder, which silently skips malformed result lines.
        with super().retrieve_embedding_batch_results(batch_id, request_options=request_options) as response:

            def results() -> typing.Iterator[EmbeddingBatchResultItem]:
                for line in response._response.iter_lines():
                    if line:
                        yield _parse_result(line)

            yield HttpResponse(response=response._response, data=results())


class _StrictAsyncRawCreateEmbeddingsClient(AsyncRawCreateEmbeddingsClient):
    @contextlib.asynccontextmanager
    async def retrieve_embedding_batch_results(
        self, batch_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.AsyncIterator[AsyncHttpResponse[typing.AsyncIterator[EmbeddingBatchResultItem]]]:
        async with super().retrieve_embedding_batch_results(batch_id, request_options=request_options) as response:

            async def results() -> typing.AsyncIterator[EmbeddingBatchResultItem]:
                async for line in response._response.aiter_lines():
                    if line:
                        yield _parse_result(line)

            yield AsyncHttpResponse(response=response._response, data=results())


class CreateEmbeddingsClientWrapper(CreateEmbeddingsClient):
    """Batch results propagate JSON, model validation, and transport errors.

    A clean end of the stream alone does not prove it contains every item.
    Compare distinct item identifiers with the batch's ``total_items``.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)
        self._raw_client = _StrictRawCreateEmbeddingsClient(client_wrapper=client_wrapper)


class AsyncCreateEmbeddingsClientWrapper(AsyncCreateEmbeddingsClient):
    """Async Batch client with the same strict result parsing as the sync client."""

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)
        self._raw_client = _StrictAsyncRawCreateEmbeddingsClient(client_wrapper=client_wrapper)
