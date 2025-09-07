from dataclasses import dataclass
from typing import Optional

from scanner.entity.system import Point3D


@dataclass(frozen=True)
class SystemStateDto:
    power: Optional[str]
    power_state: Optional[str]
    timestamp: Optional[float]


@dataclass(frozen=True)
class SystemDto:
    address: int
    name: str
    position: Point3D
    state: Optional[SystemStateDto]
