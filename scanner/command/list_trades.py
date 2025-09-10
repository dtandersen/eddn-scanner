from dataclasses import dataclass
from typing import Optional

from scanner.dto.trade import Trade
from scanner.repo.commodity_repository import PsycopgCommodityRepository


@dataclass(frozen=True)
class ListTrades:
    buy_market: int
    sell_market: Optional[int] = None
    sell_system: Optional[int] = None


@dataclass(frozen=True)
class ListTradesResult:
    trades: list[Trade]


class ListTradesHandler:
    def __init__(self, commodity_repository: PsycopgCommodityRepository):
        self.commodity_repository = commodity_repository

    def handle(self, request: ListTrades):
        trades = self.commodity_repository.get_trades(
            buy_market_id=request.buy_market,
            sell_market_id=request.sell_market,
            sell_system_id=request.sell_system,
        )
        return ListTradesResult(trades=trades)
