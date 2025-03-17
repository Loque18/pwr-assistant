from typing import TypedDict


class RagResponse(TypedDict):
    name: str
    source: str
    order_id: int
    distance: float
    text: str

