from pydantic import BaseModel, Field
from typing import Optional


class ModelMixin:
    def __str__(self):
        return repr(self)


class Object(ModelMixin, BaseModel):
    id: str = Field(alias="_id")


class ObjectWithTimestamp(ModelMixin, BaseModel):
    id: str = Field(alias="_id")
    created_at: str
    updated_at: Optional[str] = None


class PageInfo(BaseModel):
    limit_per_page: int
    page: int
    total_page: int
    total_results: int
