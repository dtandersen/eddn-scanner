from dataclasses import dataclass
from typing import List, Optional
from scanner.dto.market import MarketDto
from scanner.repo.market_repository import MarketRepository


@dataclass
class ListMarketsRequest:
    system: int
    power_state: Optional[List[str]] = None  # field(default_factory=lambda:[])
    distance: int = 20


@dataclass
class ListMarketsResult:
    markets: List[MarketDto]


class ListMarkets:
    def __init__(self, market_repository: MarketRepository):
        self.market_repository = market_repository

    def execute(self, request: ListMarketsRequest) -> ListMarketsResult:
        markets = self.market_repository.find_markets_by_system(
            request.system, request.distance, request.power_state
        )
        return ListMarketsResult(markets=markets)
