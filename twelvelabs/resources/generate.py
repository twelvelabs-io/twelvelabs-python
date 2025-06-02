import warnings
from typing import List, Literal, Optional

from ..resource import APIResource
from .. import models
from ..util import remove_none_values


class Generate(APIResource):
    def summarize(
        self,
        video_id: str,
        type: Literal["summary", "chapter", "highlight"],
        *,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> models.GenerateSummarizeResult:
        warnings.warn(
            "client.generate.summarize() is deprecated. Use client.summarize() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        json = {
            "video_id": video_id,
            "type": type,
            "prompt": prompt,
            "temperature": temperature,
        }
        res = self._post("summarize", json=remove_none_values(json), **kwargs)
        return models.GenerateSummarizeResult(**res)

    def gist(
        self,
        video_id: str,
        types: List[Literal["topic", "hashtag", "title"]],
        **kwargs,
    ) -> models.GenerateGistResult:
        warnings.warn(
            "client.generate.gist() is deprecated. Use client.gist() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        json = {
            "video_id": video_id,
            "types": types,
        }
        res = self._post("gist", json=json, **kwargs)
        return models.GenerateGistResult(**res)

    def text(
        self,
        video_id: str,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> models.GenerateOpenEndedTextResult:
        warnings.warn(
            "client.generate.text() is deprecated. Use client.analyze() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        json = {
            "video_id": video_id,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
        }
        res = self._post("generate", json=json, **kwargs)
        return models.GenerateOpenEndedTextResult(**res)

    def text_stream(
        self,
        video_id: str,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> models.GenerateOpenEndedTextStreamResult:
        warnings.warn(
            "client.generate.text_stream() is deprecated. Use client.analyze_stream() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        json = {
            "video_id": video_id,
            "prompt": prompt,
            "temperature": temperature,
            "stream": True,
        }
        res = self._post("generate", json=json, stream=True, **kwargs)
        return models.GenerateOpenEndedTextStreamResult(stream=res)
