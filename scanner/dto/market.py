from dataclasses import dataclass
from typing import Optional


@dataclass
class MarketDto:
    market_id: int
    system_address: int
    market_name: str
    system_name: str
    landing_pad: str
    distance: float
    power_state: Optional[str] = None
    power: Optional[str] = None
