import contextlib
import json
import typing

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.http_response import AsyncHttpResponse, HttpResponse
from ..core.pydantic_utilities import parse_obj_as
from ..core.request_options import RequestOptions
from ..embed.v_2.batches.client import AsyncBatchesClient, BatchesClient
from ..embed.v_2.batches.raw_client import AsyncRawBatchesClient, RawBatchesClient
from ..types.embedding_batch_result_item import EmbeddingBatchResultItem


def _parse_result(line: str) -> EmbeddingBatchResultItem:
    return parse_obj_as(EmbeddingBatchResultItem, json.loads(line))


class _StrictRawBatchesClient(RawBatchesClient):
    @contextlib.contextmanager
    def results(
        self, batch_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Iterator[HttpResponse[typing.Iterator[EmbeddingBatchResultItem]]]:
        # Keep generated authentication, HTTP errors, and response cleanup, but
        # parse each line ourselves so malformed records and validation errors
        # are not silently discarded by the generated streaming decoder.
        with super().results(batch_id, request_options=request_options) as response:

            def results() -> typing.Iterator[EmbeddingBatchResultItem]:
                for line in response._response.iter_lines():
                    if line:
                        yield _parse_result(line)

            yield HttpResponse(response=response._response, data=results())


class _StrictAsyncRawBatchesClient(AsyncRawBatchesClient):
    @contextlib.asynccontextmanager
    async def results(
        self, batch_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.AsyncIterator[AsyncHttpResponse[typing.AsyncIterator[EmbeddingBatchResultItem]]]:
        async with super().results(batch_id, request_options=request_options) as response:

            async def results() -> typing.AsyncIterator[EmbeddingBatchResultItem]:
                async for line in response._response.aiter_lines():
                    if line:
                        yield _parse_result(line)

            yield AsyncHttpResponse(response=response._response, data=results())


class EmbedV2BatchesClientWrapper(BatchesClient):
    """Batch results propagate JSON, model validation, and transport errors.

    A clean end of the stream alone does not prove it contains every item.
    Compare distinct item identifiers with the batch's ``total_items``.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)
        self._raw_client = _StrictRawBatchesClient(client_wrapper=client_wrapper)


class AsyncEmbedV2BatchesClientWrapper(AsyncBatchesClient):
    """Async Batch client with the same strict result parsing as the sync client."""

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)
        self._raw_client = _StrictAsyncRawBatchesClient(client_wrapper=client_wrapper)
