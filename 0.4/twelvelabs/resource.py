from __future__ import annotations
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import TwelveLabs


class APIResource:
    _client: TwelveLabs

    def __init__(self, client: TwelveLabs) -> None:
        self._client = client
        self._get = client.get
        self._post = client.post
        self._patch = client.patch
        self._put = client.put
        self._delete = client.delete

    def _sleep(self, seconds: float) -> None:
        time.sleep(seconds)
