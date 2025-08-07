from dataclasses import dataclass


@dataclass
class Point3D:
    x: float
    y: float
    z: float


@dataclass
class System:
    address: int
    name: str
    position: Point3D
    # market_timestamp: datetime
