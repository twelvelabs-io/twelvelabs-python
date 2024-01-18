from typing import Union, List, Literal, Optional

from ..resource import APIResource
from .. import models
from ..util import remove_none_values


class Generate(APIResource):
    def gist(
        self,
        video_id: str,
        types: List[Union[str, Literal["topic", "hashtag", "title"]]],
    ) -> models.GenerateGistResult:
        json = {
            "video_id": video_id,
            "types": types,
        }
        res = self._post("gist", json=json)
        return models.GenerateGistResult(**res)

    def summarize(
        self,
        video_id: str,
        type: Union[str, Literal["summary", "chapter", "highlight"]],
        *,
        prompt: Optional[str] = None,
    ) -> models.GenerateSummarizeResult:
        json = {
            "video_id": video_id,
            "type": type,
            "prompt": prompt,
        }
        res = self._post("summarize", json=remove_none_values(json))
        return models.GenerateSummarizeResult(**res)

    def text(
        self, video_id: str, prompt: str, **kwargs
    ) -> models.GenerateOpenEndedTextResult:
        json = {
            "video_id": video_id,
            "prompt": prompt,
        }
        res = self._post("generate", json=json, **kwargs)
        return models.GenerateOpenEndedTextResult(**res)
