from typing import List

from ._base import Object


class Engine(Object):
    author: str
    allowed_index_options: List[str]
    ready: bool
    finetune: bool
