from dataclasses import dataclass
from datetime import datetime


@dataclass
class Commodity:
    timestamp: datetime
    name: str
    buy: int
    sell: int
    supply: int
    demand: int
    station: str
    system: str
