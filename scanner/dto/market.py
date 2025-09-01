from dataclasses import dataclass


@dataclass
class MarketDto:
    market_id: int
    system_address: int
    market_name: str
    system_name: str
    landing_pad: str
