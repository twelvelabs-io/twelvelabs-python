# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class IndexesCreateRequestModelsItem(UniversalBaseModel):
    model_name: str = pydantic.Field()
    """
    The name of the model. The following models are available:
    
      - **Embedding**: These models are proficient at performing tasks such as search and classification, enabling enhanced video understanding.
    
        - `marengo2.7`
    
      - **Generative**: These models generate text based on your videos.
    
        - `pegasus1.2`
    
    <Note title="Note">
    You cannot change the models once the index has been created.
    </Note>
    
    For more details, see the [Video understanding models](/v1.3/docs/concepts/models) page.
    """

    model_options: typing.List[str] = pydantic.Field()
    """
    An array that specifies how the platform will process the videos uploaded to this index. For the Marengo and Pegasus models, you can specify one or both of the following model options: `visual` and `audio`. For more details, see the [model options](/v1.3/docs/concepts/model-options) page.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
