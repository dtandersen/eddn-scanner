from datetime import datetime
from typing import Any
from scanner.entity.commodity import Commodity
from scanner.entity.market import Market
from scanner.entity.system import Point3D, System
from scanner.repo.commodity_repository import PsycopgCommodityRepository
from scanner.repo.market_repository import PsycopgMarketRepository
from scanner.repo.system_repository import PsycopgSystemRepository


def nottest(obj: Any):
    obj.__test__ = False
    return obj


@nottest
class TestFacade:
    def __init__(
        self,
        system_repository: PsycopgSystemRepository,
        market_repository: PsycopgMarketRepository,
        commodity_repository: PsycopgCommodityRepository,
    ):
        self.system_repository = system_repository
        self.market_repository = market_repository
        self.commodity_repository = commodity_repository

    def given_system(self, address: int, name: str, position: Point3D):
        system = System(address=address, name=name, position=position)
        self.system_repository.create(system)

    def given_market(
        self,
        market_id: int,
        system_address: int,
        name: str,
        last_updated: datetime | None = None,
        station_type: str | None = None,
        docking_access: str | None = None,
    ):
        market = Market(
            market_id=market_id,
            system_address=system_address,
            name=name,
            last_updated=last_updated,
            station_type=station_type,
            docking_access=docking_access,
        )
        self.market_repository.create(market)

    def given_commodity(
        self,
        market_id: int,
        name: str,
        buy: int = 0,
        sell: int = 0,
        supply: int = 0,
        demand: int = 0,
    ):
        commodity = Commodity(
            market_id=market_id,
            name=name,
            buy=buy,
            sell=sell,
            supply=supply,
            demand=demand,
        )
        self.commodity_repository.create(commodity)
