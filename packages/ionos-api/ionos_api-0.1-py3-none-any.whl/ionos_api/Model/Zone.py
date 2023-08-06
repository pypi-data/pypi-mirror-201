from dataclasses import dataclass


@dataclass
class Zone(object):
    id: str
    name: str
    type: str
