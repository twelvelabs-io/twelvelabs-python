from typing import List, Union, BinaryIO, Optional, Literal

from ._base import BaseModel, Object


class CreateEmbeddingsTaskVideoParams:
    file: Union[str, BinaryIO, None]
    url: Optional[str]
    start_offset_sec: Optional[float]
    end_offset_sec: Optional[float]
    clip_length: Optional[int]
    scopes: Optional[List[Literal["clip", "video"]]]


class Embedding(BaseModel):
    float: List[float]


class CreateEmbeddingsResult(BaseModel):
    engine_name: str
    text_embedding: Embedding


class EmbeddingsTaskStatus(Object):
    engine_name: str
    status: str


class VideoEmbedding(BaseModel):
    start_offset_sec: float
    end_offset_sec: float
    embedding_scope: str
    embedding: Embedding


class EmbeddingsTask(Object):
    engine_name: str
    status: str
    video_embeddings: Optional[List[VideoEmbedding]] = None
