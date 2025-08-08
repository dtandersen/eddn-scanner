from abc import ABCMeta, abstractmethod
from datetime import datetime
import json
import logging
from typing import Any, Dict

from dacite import Config, from_dict


# from scanner import scanner
from scanner.command.update_commodities import UpdateCommodities, AddCommodityRequest
from scanner.command.update_system import UpdateSystem, UpdateSystemRequest
from scanner.entity.commodity import Commodity
from scanner.entity.system import Point3D
from scanner.event.commodity import CommoditiesEvent, CommodityEvent
from scanner.event.discovery import DiscoveryEvent
from scanner.event.event_handler import EventBus
from scanner.repo.commodity_repository import CommodityRepository
from scanner.repo.market_repository import MarketRepository
from scanner.repo.system_repository import SystemRepository

# import scanner

EddnEvent = Dict[str, Any]


class EddnHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, event: EddnEvent):
        pass


class CommodityWriter:
    log = logging.getLogger(__name__)

    def __init__(
        self,
        events: EventBus,
        commodity_repository: CommodityRepository,
        market_repository: MarketRepository,
        system_repository: SystemRepository,
    ):
        events.commodities.add_delegate(self.on_commodities)
        events.discovery.add_delegate(self.on_discovery)

        self.commodity_repository = commodity_repository
        self.market_repository = market_repository
        self.system_repository = system_repository

    def on_commodities(self, event: CommoditiesEvent):
        timestamp = datetime.fromisoformat(event.message.timestamp)
        command = UpdateCommodities(
            self.commodity_repository, self.market_repository, self.system_repository
        )
        command.execute(
            AddCommodityRequest(
                market_id=event.message.marketId,
                station=event.message.stationName,
                docking_access=event.message.carrierDockingAccess,
                station_type=event.message.stationType,
                system=event.message.systemName,
                timestamp=timestamp,
                commodities=[
                    self.map_to_commodity(
                        c,
                        event.message.marketId,
                    )
                    for c in event.message.commodities
                ],
            )
        )

    def on_discovery(self, event: DiscoveryEvent):
        command = UpdateSystem(self.system_repository)
        command.execute(
            UpdateSystemRequest(
                address=event.message.SystemAddress,
                name=event.message.SystemName,
                position=Point3D(
                    event.message.StarPos[0],
                    event.message.StarPos[1],
                    event.message.StarPos[2],
                ),
            )
        )

    def map_to_commodity(self, event: CommodityEvent, market_id: int) -> Commodity:
        return Commodity(
            market_id=market_id,
            name=event.name,
            buy=event.buyPrice,
            sell=event.sellPrice,
            supply=event.stock,
            demand=event.demand,
        )


class CommodityEddnHandler(EddnHandler):
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def handle(self, event: EddnEvent):
        schema = event.get("$schemaRef")
        if schema == "https://eddn.edcd.io/schemas/commodity/3":
            discovery_event = from_dict(
                data_class=CommoditiesEvent,
                data=event,
                config=Config(strict=False, convert_key=fix_schema_ref),
            )
            self.event_bus.commodities.publish(discovery_event)
        elif schema == "https://eddn.edcd.io/schemas/fssdiscoveryscan/1":
            discovery_event = from_dict(
                data_class=DiscoveryEvent,
                data=event,
                config=Config(strict=False, convert_key=fix_schema_ref),
            )
            self.event_bus.discovery.publish(discovery_event)


class LoggingEddnHandler(EddnHandler):
    log = logging.getLogger(__name__)

    def __init__(self, filter: list[str] | None = None):
        self.filter = filter

    def handle(self, event: EddnEvent):
        schema = event.get("$schemaRef")
        if self.filter and schema not in self.filter:
            return

        self.log.info(f"{json.dumps(event, indent=2)}\n---")


def fix_schema_ref(key: str) -> str:
    if key == "schemaRef":
        return "$schemaRef"
    else:
        return key
