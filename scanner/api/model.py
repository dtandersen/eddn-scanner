from dataclasses import dataclass


@dataclass(frozen=True)
class ListTradesRequest:
    buy_market: int
    sell_market: int


@dataclass(frozen=True)
class TradeModel:
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


@dataclass(frozen=True)
class ListTradesResult:
    trades: list[TradeModel]


@dataclass(frozen=True)
class ListTradesResult2:
    result: ListTradesResult
