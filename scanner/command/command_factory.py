from scanner.command.get_system import GetSystem
from scanner.command.list_markets import ListMarkets
from scanner.command.list_systems import ListSystems
from scanner.command.update_commodities import UpdateCommodities
from scanner.command.update_system import UpdateSystem
from scanner.repo.commodity_repository import CommodityRepository
from scanner.repo.market_repository import MarketRepository
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import SystemRepository
from scanner.repo.system_state_repository import SystemStateRepository


class CommandFactory:
    def __init__(
        self,
        system_repository: SystemRepository,
        market_repository: MarketRepository,
        commodity_repository: CommodityRepository,
        power_repository: PsycopgPowerRepository,
        system_state_repository: SystemStateRepository,
    ):
        self.system_repository = system_repository
        self.market_repository = market_repository
        self.commodity_repository = commodity_repository
        self.power_repository = power_repository
        self.system_state_repository = system_state_repository

    def update_system(self):
        return UpdateSystem(
            system_repository=self.system_repository,
            power_repository=self.power_repository,
            system_state_repository=self.system_state_repository,
        )

    def update_commodities(self):
        return UpdateCommodities(
            commodity_repository=self.commodity_repository,
            market_repository=self.market_repository,
            system_repository=self.system_repository,
        )

    def get_system(self):
        return GetSystem(
            system_repository=self.system_repository,
            system_state_repository=self.system_state_repository,
        )

    def list_systems(self):
        return ListSystems(
            system_repository=self.system_repository,
        )

    def list_markets(self):
        return ListMarkets(
            market_repository=self.market_repository,
        )
