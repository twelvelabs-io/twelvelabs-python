from typing import TypedDict, Literal, List


class IndexModel(TypedDict):
    name: Literal["marengo2.7", "pegasus1.1"]
    options: List[Literal["visual", "audio"]]
