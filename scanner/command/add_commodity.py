from dataclasses import dataclass
from scanner.entity.commodity import Commodity
from scanner.repo.commodity_repository import CommodityRepository
from scanner.repo.market_repository import MarketRepository


@dataclass
class AddCommodityRequest:
    market_id: int
    commodities: list[Commodity]


class AddCommodity:
    def __init__(
        self,
        commodity_repository: CommodityRepository,
        market_repository: MarketRepository,
    ):
        self.commodity_repository = commodity_repository
        self.market_repository = market_repository

    def execute(self, request: AddCommodityRequest):
        self.commodity_repository.delete_market(request.market_id)

        for commodity in request.commodities:
            self.commodity_repository.create(commodity)
