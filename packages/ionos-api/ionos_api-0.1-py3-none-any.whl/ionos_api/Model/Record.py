from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from .Zone import Zone


@dataclass(kw_only=True)
class RecordDefinition(object):
    name: str
    type: str
    content: str
    ttl: int = 3600
    prio: Optional[int] = None
    disabled: bool = False

    def __eq__(self, other):
        return self.name == other.name \
           and self.type == other.type \
           and self.content == other.content


@dataclass(kw_only=True)
class Record(RecordDefinition):
    id: str
    rootName: str
    changeDate: datetime

