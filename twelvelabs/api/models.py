from typing import BinaryIO, List, Optional, TypedDict, Union

from pydantic import BaseModel, Field


class ModelMixin:
    def __str__(self):
        return repr(self)


class Object(ModelMixin, BaseModel):
    id: str = Field(alias="_id")
    created_at: str
    updated_at: str


class Engine(Object):
    author: str
    allowed_index_options: List[str]
    ready: bool
    finetune: bool


class ClassifyLabel(TypedDict):
    name: str
    prompts: List[str]


class VideoFile(TypedDict):
    file: Union[str, BinaryIO, None]
    url: Optional[str]
    transcription_file: Union[str, BinaryIO]
    transcription_url: Optional[str]
    language: Optional[str]
