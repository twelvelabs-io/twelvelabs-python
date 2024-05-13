from typing import List, Optional, Any, Union, Literal, TYPE_CHECKING
from pydantic import PrivateAttr

from ._base import BaseModel, TokenPageInfo, RootModelList

if TYPE_CHECKING:
    from ..resources import Classify as ClassifyResource


class ClassifyClassParams:
    name: str
    prompts: List[str]
    options: Optional[
        List[Union[str, Literal["visual", "conversation", "text_in_video", "logo"]]]
    ] = None
    conversation_option: Optional[Union[str, Literal["semantic", "exact_match"]]] = None


class ClassifyDetailedScore(BaseModel):
    max_score: str
    avg_score: str
    normalized_score: str


class ClassifyClip(BaseModel):
    start: int
    end: int
    score: float
    option: str
    prompt: str
    thumbnail_url: Optional[str] = None
    detailed_scores: Optional[ClassifyDetailedScore] = None


class ClassifyClass(BaseModel):
    name: str
    score: str
    duration_ratio: str
    clips: List[Any]


class ClassifyVideoData(BaseModel):
    video_id: str
    classes: List[ClassifyClass]


class ClassifyResult(BaseModel):
    data: List[ClassifyVideoData]


class ClassifyPageResult(BaseModel):
    _resource: ClassifyResource = PrivateAttr()
    data: List[ClassifyVideoData]
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
