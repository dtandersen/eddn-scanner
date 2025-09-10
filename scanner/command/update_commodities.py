from dataclasses import dataclass
from datetime import datetime
import logging
from scanner.entity.commodity import Commodity
from scanner.entity.market import Market
from scanner.repo.commodity_repository import CommodityRepository
from scanner.repo.market_repository import MarketRepository, ResourceNotFoundError
from scanner.repo.system_repository import SystemRepository


@dataclass
class UpdateCommodities:
    market_id: int
    timestamp: datetime
    system: str
    station: str
    commodities: list[Commodity]
    station_type: str | None = None
    docking_access: str | None = None


class UpdateMarketCommoditiesHandler:
    log = logging.getLogger(__name__)

    def __init__(
        self,
        commodity_repository: CommodityRepository,
        market_repository: MarketRepository,
        system_repository: SystemRepository,
    ):
        self.commodity_repository = commodity_repository
        self.market_repository = market_repository
        self.system_repository = system_repository

    def handle(self, request: UpdateCommodities):
        self.log.info(f"Updating commodities for {request.system}/{request.station}")
        try:
            market = self.market_repository.get_market(request.market_id)
            if (
                request.docking_access is not None
                and market.docking_access != request.docking_access
            ):
                self.log.info(
                    f"Updating docking access for market {request.market_id} from {market.docking_access} to {request.docking_access}"
                )
                # market.docking_access = request.docking_access
                self.market_repository.update_docking_access(
                    request.market_id, request.docking_access
                )

            if (
                request.station_type is not None
                and market.station_type != request.station_type
            ):
                self.log.info(
                    f"Updating station type for market {request.market_id} from {market.station_type} to {request.station_type}"
                )
                self.market_repository.update_station_type(
                    request.market_id, request.station_type
                )
        except ResourceNotFoundError as _e:
            try:
                self.add_market(
                    request.market_id,
                    request.station,
                    request.system,
                    request.station_type,
                    request.docking_access,
                )
            except ResourceNotFoundError as e:
                self.log.warning(e)
                return

        self.commodity_repository.delete_market(request.market_id)
        self.market_repository.update_timestamp(request.market_id, request.timestamp)

        for commodity in request.commodities:
            self.commodity_repository.create(commodity)

    def add_market(
        self,
        market_id: int,
        station_name: str,
        system_name: str,
        station_type: str | None,
        docking_access: str | None,
    ):
        try:
            system = self.system_repository.get_system_by_name(system_name)
        except ResourceNotFoundError as e:
            raise e
        # system = self.system_repository.get_system_by_name(system_name)
        market = Market(
            market_id=market_id,
            system_address=system.address,
            name=station_name,
            station_type=station_type,
            docking_access=docking_access,
            last_updated=None,
        )
        self.market_repository.create(market)
