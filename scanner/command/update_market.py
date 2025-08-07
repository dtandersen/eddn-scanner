from dataclasses import dataclass
import logging
from scanner.repo.market_repository import MarketRepository
from scanner.repo.system_repository import SystemRepository


@dataclass
class UpdateMarketRequest:
    market_id: int


class UpdateMarket:
    log = logging.getLogger(__name__)

    def __init__(
        self,
        market_repository: MarketRepository,
        system_repository: SystemRepository,
    ):
        self.system_repository = system_repository
        self.market_repository = market_repository

    def execute(self, request: UpdateMarketRequest):
        pass
