from dataclasses import dataclass
from typing import List, Optional
from scanner.dto.market import MarketDto
from scanner.repo.market_repository import MarketRepository


@dataclass
class ListMarketsRequest:
    system: int
    distance: Optional[int] = None


@dataclass
class ListMarketsResult:
    markets: List[MarketDto]


class ListMarkets:
    def __init__(self, market_repository: MarketRepository):
        self.market_repository = market_repository

    def execute(self, request: ListMarketsRequest) -> ListMarketsResult:
        markets = self.market_repository.find_markets_by_system(
            request.system, request.distance
        )
        return ListMarketsResult(markets=markets)
