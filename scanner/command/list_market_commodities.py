from dataclasses import dataclass

from scanner.entity.commodity import Commodity
from scanner.repo.commodity_repository import CommodityRepository


@dataclass
class ListMarketCommodities:
    market_id: int


@dataclass
class ListMarketCommoditiesResult:
    commodities: list[Commodity]


class ListMarketCommoditiesHandler:
    def __init__(self, commodity_repository: CommodityRepository):
        self.commodity_repository = commodity_repository

    def handle(self, request: ListMarketCommodities):
        all_commodities = self.commodity_repository.all()
        market_commodities = [
            commodity
            for commodity in all_commodities
            if commodity.market_id == request.market_id
        ]
        return ListMarketCommoditiesResult(commodities=market_commodities)
