# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class IndexModelsItem(UniversalBaseModel):
    model_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    A string representing the name of the model.
    """

    model_options: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    An array of strings that contains the [model options](/v1.3/docs/concepts/modalities#model-options) enabled for this index.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
