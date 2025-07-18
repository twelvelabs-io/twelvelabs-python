# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
import typing_extensions
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ..core.serialization import FieldMetadata
from .index_models_item import IndexModelsItem


class IndexSchema(UniversalBaseModel):
    """
    An index groups one or more videos stored as vectors and is the most granular level at which you can perform a search.
    """

    id: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="_id")] = pydantic.Field(default=None)
    """
    A string representing the unique identifier of the index. It is assigned by the API when an index is created.
    """

    created_at: typing.Optional[str] = pydantic.Field(default=None)
    """
    A string representing the date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), that the index was created.
    """

    updated_at: typing.Optional[str] = pydantic.Field(default=None)
    """
    A string representing the date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), that the index has been updated.
    """

    expires_at: typing.Optional[str] = pydantic.Field(default=None)
    """
    A string representing the date and time, in the RFC 3339 format ("YYYY-MM-DDTHH:mm:ssZ"), when your index will expire.
    
    If you're on the Free plan, the platform retains your index data for 90 days from creation. After this period, the platform deletes your index data, and this action cannot be undone. To continue using your index beyond this period, consider upgrading to the Developer plan, which offers unlimited index retention. For details, see the [Upgrade your plan](/v1.3/docs/get-started/manage-your-plan#upgrade-your-plan) section.
    
    If you're on the Developer plan, this field is set to `null`, indicating no expiration.
    """

    index_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    A string representing the name of the index.
    """

    total_duration: typing.Optional[float] = pydantic.Field(default=None)
    """
    A number representing the total duration, in seconds, of the videos in the index.
    """

    video_count: typing.Optional[float] = pydantic.Field(default=None)
    """
    The number of videos uploaded to this index.
    """

    models: typing.Optional[typing.List[IndexModelsItem]] = pydantic.Field(default=None)
    """
    An array containing the list of the [video understanding models](/v1.3/docs/concepts/models) enabled for this index.
    """

    addons: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    The list of the add-ons that are enabled for this index.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
