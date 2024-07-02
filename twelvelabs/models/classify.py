from __future__ import annotations

from typing import List, Optional, Union, Literal, TYPE_CHECKING
from pydantic import PrivateAttr

from ._base import BaseModel, TokenPageInfo, RootModelList

if TYPE_CHECKING:
    from ..resources import Classify as ClassifyResource


class ClassifyClassParams:
    name: str
    prompts: List[str]
    options: Optional[
        List[Union[str, Literal["visual", "conversation", "text_in_video"]]]
    ] = None
    conversation_option: Optional[Union[str, Literal["semantic", "exact_match"]]] = None

    def __init__(
        self,
        name: str,
        prompts: List[str],
        *,
        options: Optional[
            List[Union[str, Literal["visual", "conversation", "text_in_video"]]]
        ] = None,
        conversation_option: Optional[
            Union[str, Literal["semantic", "exact_match"]]
        ] = None,
    ):
        self.name = name
        self.prompts = prompts
        self.options = options
        self.conversation_option = conversation_option


class ClassifyDetailedScore(BaseModel):
    max_score: float
    avg_score: float
    normalized_score: float


class ClassifyClip(BaseModel):
    start: float
    end: float
    score: float
    option: str
    prompt: str
    thumbnail_url: Optional[str] = None


class ClassifyClass(BaseModel):
    name: str
    score: float
    duration_ratio: float
    clips: Optional[RootModelList[ClassifyClip]] = None
    detailed_scores: Optional[ClassifyDetailedScore] = None


class ClassifyVideoData(BaseModel):
    video_id: str
    classes: RootModelList[ClassifyClass]


class ClassifyPageResult(BaseModel):
    _resource: ClassifyResource = PrivateAttr()
    data: RootModelList[ClassifyVideoData]
    page_info: TokenPageInfo

    def __init__(self, resource: ClassifyResource, **data):
        super().__init__(**data)
        self._resource = resource

    def __iter__(self):
        return self

    def __next__(self) -> RootModelList[ClassifyVideoData]:
        next_page_token = self.page_info.next_page_token
        if not next_page_token:
            raise StopIteration

        res = self._resource.by_page_token(next_page_token)
        self.page_info = res.page_info
        return res.data
