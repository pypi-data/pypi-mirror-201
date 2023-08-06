from dataclasses import asdict, field
from typing import Any, List

from marshmallow_dataclass import dataclass as ma_dataclass


@ma_dataclass
class PageableResponse:
    items: List[Any] = field(default_factory=list)
    num_items: int = 0
    total_items: int = 0

    def __post_init__(self):
        self.num_items = len(self.items)

    def asdict(self):
        return asdict(self)


# -- Offset PAGEABLE -- #
@ma_dataclass
class OffsetPageableResponse(PageableResponse):
    pass


@ma_dataclass
class OffsetPageableQueryParameters:
    offset: int = 0
    limit: int = 100
