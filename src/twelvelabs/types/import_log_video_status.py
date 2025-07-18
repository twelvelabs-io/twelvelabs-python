# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class ImportLogVideoStatus(UniversalBaseModel):
    """
    Counts of files in different statuses. See the [Task object](/v1.3/api-reference/tasks/the-task-object) page for details on each status.
    """

    ready: int
    validating: int
    queued: int
    pending: int
    indexing: int
    failed: int

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
