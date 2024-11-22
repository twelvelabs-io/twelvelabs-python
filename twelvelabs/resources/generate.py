from typing import Union, List, Literal, Optional

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
        json = {
            "video_id": video_id,
            "type": type,
            "prompt": prompt,
            "temperature": temperature,
        }
        res = self._post("summarize", json=remove_none_values(json), **kwargs)
        return models.GenerateSummarizeResult(**res)

    def text(
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
        json = {
            "video_id": video_id,
            "prompt": prompt,
            "temperature": temperature,
            "stream": True,
        }
        res = self._post("generate", json=json, stream=True, **kwargs)
        return models.GenerateOpenEndedTextStreamResult(stream=res)
