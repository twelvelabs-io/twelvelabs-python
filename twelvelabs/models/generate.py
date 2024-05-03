from typing import List, Optional

from ._base import BaseModel, RootModelList


class GenerateOpenEndedTextResult(BaseModel):
    id: str
    data: str


class GenerateSummarizeChapterResult(BaseModel):
    chapter_number: int
    start: int
    end: int
    chapter_title: str
    chapter_summary: str


class GenerateSummarizeHighlightResult(BaseModel):
    start: int
    end: int
    highlight: str


class GenerateSummarizeResult(BaseModel):
    id: str
    summary: Optional[str] = None
    chapters: Optional[RootModelList[GenerateSummarizeChapterResult]] = None
    highlights: Optional[RootModelList[GenerateSummarizeHighlightResult]] = None


class GenerateGistResult(BaseModel):
    id: str
    title: Optional[str] = None
    topics: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
