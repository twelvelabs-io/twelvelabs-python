# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
import typing_extensions
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ..core.serialization import FieldMetadata
from .video_vector_system_metadata import VideoVectorSystemMetadata


class VideoVector(UniversalBaseModel):
    """
    A video object that contains information about the video.
    """

    id: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="_id")] = pydantic.Field(default=None)
    """
    A string representing the unique identifier of a video. The platform creates a new `video_vector` object and assigns it a unique identifier when the video has successfully been indexed. Note that video IDs are different from task IDs.
    """

    created_at: typing.Optional[str] = pydantic.Field(default=None)
    """
    A string indicating the date and time, in the RFC RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), that the video indexing task was created.
    """

    updated_at: typing.Optional[str] = pydantic.Field(default=None)
    """
    A string indicating the date and time, in the RFC RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), that the video indexing task object was last updated. The platform updates this field every time the video indexing task transitions to a different state.
    """

    indexed_at: typing.Optional[str] = pydantic.Field(default=None)
    """
    A string indicating the date and time, in the RFC RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), that the video indexing task has been completed.
    """

    system_metadata: typing.Optional[VideoVectorSystemMetadata] = pydantic.Field(default=None)
    """
    System-generated metadata about the video.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
