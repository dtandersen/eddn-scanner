from dataclasses import dataclass


@dataclass(frozen=True)
class Trade:
    buy_market_id: int
    buy_market_name: str
    sell_market_id: int
    sell_market_name: str
    commodity: str
    buy: int
    sell: int
    supply: int
    demand: int
    profit: int
    distance: float
