from typing import List

from ..models import RootModelList
from ..resource import APIResource
from .. import models


class Engine(APIResource):
    def retrieve(self, id: str, **kwargs) -> models.Engine:
        res = self._get(f"engines/{id}", **kwargs)
        return models.Engine(**res)

    def list(self, **kwargs) -> RootModelList[models.Engine]:
        res = self._get("engines", **kwargs)
        return RootModelList([models.Engine(**engine) for engine in res["data"]])
