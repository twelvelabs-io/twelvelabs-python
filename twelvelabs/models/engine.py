from typing import List

from ._base import Object


class Engine(Object):
    author: str
    allowed_engine_options: List[str]
    ready: bool
    finetune: bool
