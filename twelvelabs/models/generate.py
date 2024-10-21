import httpx
import json
from typing import List, Optional
from pydantic import PrivateAttr

from ._base import BaseModel, RootModelList


class GenerateOpenEndedTextResult(BaseModel):
    id: str
    data: str


class GenerateSummarizeChapterResult(BaseModel):
    chapter_number: int
    start: float
    end: float
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
    topics: Optional[RootModelList[str]] = None
    hashtags: Optional[RootModelList[str]] = None


class GenerateOpenEndedTextStreamResult(BaseModel):
    _stream: httpx.Response = PrivateAttr()
    id: str = ""
    texts: List[str] = []
    aggregated_text: str = ""

    def __init__(self, stream: httpx.Response, **data):
        super().__init__(**data)
        self._stream = stream
        self.id = ""
        self.texts = []
        self.aggregated_text = ""

    def add_text(self, text: str):
        self.texts.append(text)
        self.aggregated_text += text

    def __iter__(self):
        buffer = ""
        with self._stream as response:
            for line in response.iter_lines():
                buffer += line
                while True:
                    try:
                        # Try to decode a JSON object from the buffer
                        event, index = json.JSONDecoder().raw_decode(buffer)
                        # Update the buffer to remove the decoded JSON object
                        buffer = buffer[index:].lstrip()
                    except json.JSONDecodeError:
                        break

                    if "code" in event:
                        # Handle non-stream error
                        raise Exception(event["message"])
                    elif event["event_type"] == "stream_start":
                        self.id = event["metadata"]["generation_id"]
                    elif event["event_type"] == "stream_error":
                        raise Exception(event["error"]["message"])
                    elif event["event_type"] == "text_generation":
                        self.add_text(event["text"])
                        yield event["text"]
                    elif event["event_type"] == "stream_end":
                        return

            if buffer:
                # If there's any remaining data in the buffer, process it
                event = json.loads(buffer)
                if event["event_type"] == "text_generation":
                    self.add_text(event["text"])
                    yield event["text"]
