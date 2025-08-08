from dataclasses import dataclass
from typing import List

from scanner.event.event import EddnEvent


@dataclass
class DiscoveryMessage:
    SystemAddress: int
    SystemName: str
    StarPos: List[float]


@dataclass
class DiscoveryEvent(EddnEvent):
    message: DiscoveryMessage
