# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
import typing_extensions
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ....core.serialization import FieldMetadata
from .tasks_status_response_video_embedding import TasksStatusResponseVideoEmbedding


class TasksStatusResponse(UniversalBaseModel):
    id: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="_id")] = pydantic.Field(default=None)
    """
    The unique identifier of the video embedding task.
    """

    status: typing.Optional[str] = pydantic.Field(default=None)
    """
    A string indicating the status of the video indexing task. It can take one of the following values: `processing`, `ready` or `failed`.
    """

    model_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The name of the video understanding model the platform used to create the embedding.
    """

    video_embedding: typing.Optional[TasksStatusResponseVideoEmbedding] = pydantic.Field(default=None)
    """
    An object containing the metadata associated with the embedding.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
