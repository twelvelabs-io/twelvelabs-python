import os
from typing import Union, Literal, List, Optional

from .constants import BASE_URL, LATEST_API_VERSION
from .base_client import APIClient
from . import resources
from . import models
from .util import remove_none_values


class TwelveLabs(APIClient):
    index: resources.Index
    task: resources.Task
    search: resources.Search
    generate: resources.Generate
    embed: resources.Embed

    base_url: str
    api_key: str

    def __init__(
        self,
        api_key: str,
        version: Union[
            str,
            Literal["v1.1", "v1.2", "v1.3"],
        ] = LATEST_API_VERSION,
    ) -> None:
        if version != LATEST_API_VERSION:
            print(
                f"[Warning] You manually set the API version to {version}, but this SDK version is not fully compatible with current API version, please use version 0.3.x or earlier"
            )
        assert (
            api_key,
            "Provide `api_key` to initialize a client. You can see the API Key in the Dashboard page: https://dashboard.playground.io",
        )
        base_url = f"{BASE_URL}/{version}/"
        custom_base_url = os.environ.get("TWELVELABS_BASE_URL")
        if custom_base_url is not None:
            base_url = f"{custom_base_url}/{version}/"

        self.base_url = base_url
        self.api_key = api_key
        super().__init__(base_url, api_key)

        self.index = resources.Index(self)
        self.task = resources.Task(self)
        self.search = resources.Search(self)
        self.generate = resources.Generate(self)
        self.embed = resources.Embed(self)

    def summarize(
        self,
        video_id: str,
        type: Literal["summary", "chapter", "highlight"],
        *,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> models.GenerateSummarizeResult:
        json = {
            "video_id": video_id,
            "type": type,
            "prompt": prompt,
            "temperature": temperature,
        }
        res = self.generate._post("summarize", json=remove_none_values(json), **kwargs)
        return models.GenerateSummarizeResult(**res)

    def gist(
        self,
        video_id: str,
        types: List[Literal["topic", "hashtag", "title"]],
        **kwargs,
    ) -> models.GenerateGistResult:
        json = {
            "video_id": video_id,
            "types": types,
        }
        res = self.generate._post("gist", json=json, **kwargs)
        return models.GenerateGistResult(**res)

    def analyze(
        self,
        video_id: str,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> models.GenerateOpenEndedTextResult:
        json = {
            "video_id": video_id,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
        }
        res = self.generate._post("analyze", json=json, **kwargs)
        return models.GenerateOpenEndedTextResult(**res)

    def analyze_stream(
        self,
        video_id: str,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> models.GenerateOpenEndedTextStreamResult:
        json = {
            "video_id": video_id,
            "prompt": prompt,
            "temperature": temperature,
            "stream": True,
        }
        res = self.generate._post("analyze", json=json, stream=True, **kwargs)
        return models.GenerateOpenEndedTextStreamResult(stream=res)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass
