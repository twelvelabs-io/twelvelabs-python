import typing
import os

from .base_client import BaseClient, AsyncBaseClient
from .wrapper.search_client_wrapper import SearchClientWrapper, AsyncSearchClientWrapper
from .wrapper.task_client_wrapper import TaskClientWrapper, AsyncTaskClientWrapper
from .wrapper.embed_client_wrapper import EmbedClientWrapper, AsyncEmbedClientWrapper
from .wrapper.index_client_wrapper import (
    IndexesClientWrapper,
    AsyncIndexesClientWrapper,
)

OMIT = typing.cast(typing.Any, ...)


class TwelveLabs(BaseClient):
    def __init__(
        self,
        *,
        api_key: typing.Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize the TwelveLabs client.

        Parameters
        ----------
        api_key : str, optional
            The API key for authentication with TwelveLabs API.
            If not provided, the TWELVE_LABS_API_KEY environment variable will be used.
        **kwargs : dict
            Additional parameters to pass to the BaseClient
        """
        if api_key:
            kwargs["api_key"] = api_key

        if os.getenv("TWELVELABS_BASE_URL"):
            kwargs["base_url"] = os.getenv("TWELVELABS_BASE_URL")

        super().__init__(**kwargs)

        self.search = SearchClientWrapper(client_wrapper=self._client_wrapper)
        self.tasks = TaskClientWrapper(client_wrapper=self._client_wrapper)
        self.embed = EmbedClientWrapper(client_wrapper=self._client_wrapper)
        self.indexes = IndexesClientWrapper(client_wrapper=self._client_wrapper)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class AsyncTwelveLabs(AsyncBaseClient):
    def __init__(
        self,
        *,
        api_key: typing.Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize the AsyncTwelveLabs client.

        Parameters
        ----------
        api_key : str, optional
            The API key for authentication with TwelveLabs API.
            If not provided, the TWELVE_LABS_API_KEY environment variable will be used.
        **kwargs : dict
            Additional parameters to pass to the AsyncBaseClient
        """
        if api_key:
            kwargs["api_key"] = api_key

        if os.getenv("TWELVELABS_BASE_URL"):
            kwargs["base_url"] = os.getenv("TWELVELABS_BASE_URL")

        super().__init__(**kwargs)

        self.search = AsyncSearchClientWrapper(client_wrapper=self._client_wrapper)
        self.tasks = AsyncTaskClientWrapper(client_wrapper=self._client_wrapper)
        self.embed = AsyncEmbedClientWrapper(client_wrapper=self._client_wrapper)
        self.indexes = AsyncIndexesClientWrapper(client_wrapper=self._client_wrapper)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass
