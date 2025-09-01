from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Progress:
    ConflictProgress: float
    Power: str


@dataclass
class FSDJumpEventMessage:
    timestamp: str
    SystemAddress: int
    StarSystem: str
    StarPos: List[float]
    PowerplayState: Optional[str]
    ControllingPower: Optional[str]
    PowerplayConflictProgress: List[Progress] = field(default_factory=lambda: [])


@dataclass
class FSDJumpEvent:
    message: FSDJumpEventMessage
