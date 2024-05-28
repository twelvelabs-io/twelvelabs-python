from typing import List

from ._base import BaseModel, Object


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
    video_embeddings: List[VideoEmbedding]
