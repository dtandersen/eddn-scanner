from dataclasses import dataclass
from scanner.entity.commodity import Commodity
from scanner.repo.commodity_repository import CommodityRepository


@dataclass
class AddCommodityRequest:
    commodities: list[Commodity]


class AddCommodity:
    def __init__(self, commodity_repository: CommodityRepository):
        self.commodity_repository = commodity_repository

    def execute(self, request: AddCommodityRequest):
        for commodity in request.commodities:
            self.commodity_repository.create(commodity)
