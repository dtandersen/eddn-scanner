from dataclasses import dataclass


@dataclass(frozen=True)
class Commodity:
    market_id: int
    name: str
    buy: int
    sell: int
    supply: int
    demand: int
