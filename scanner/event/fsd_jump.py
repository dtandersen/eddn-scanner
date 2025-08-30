from dataclasses import dataclass
from typing import List


@dataclass
class Progress:
    ConflictProgress: float
    Power: str


@dataclass
class FSDJumpEventMessage:
    SystemAddress: int
    PowerplayState: str
    PowerplayConflictProgress: List[Progress]


@dataclass
class FSDJumpEvent:
    message: FSDJumpEventMessage
