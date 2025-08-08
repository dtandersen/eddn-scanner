from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Market:
    market_id: int
    system_address: int
    name: str
    last_updated: datetime | None
    station_type: str | None = None
    docking_access: str | None = None
