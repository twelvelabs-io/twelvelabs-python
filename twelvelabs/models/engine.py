from typing import List

from ._base import ObjectWithTimestamp


class Engine(ObjectWithTimestamp):
    author: str
    allowed_index_options: List[str]
    ready: bool
    finetune: bool
