from abc import ABCMeta, abstractmethod
from datetime import datetime
import json
import logging
from typing import Any, Dict

from dacite import Config, from_dict

# from scanner import scanner
from scanner.command.update_commodities import UpdateCommodities, AddCommodityRequest
from scanner.entity.commodity import Commodity
from scanner.event.commodity import CommoditiesEvent, CommodityEvent
from scanner.event.event_handler import EventBus
from scanner.repo.commodity_repository import CommodityRepository
from scanner.repo.market_repository import MarketRepository

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
    ):
        events.commodities.add_delegate(self.on_commodities)
        self.commodity_repository = commodity_repository
        self.market_repository = market_repository

    def on_commodities(self, event: CommoditiesEvent):
        self.log.info(
            f"Updating commodities for {event.message.systemName}/{event.message.stationName}"
        )
        timestamp = datetime.fromisoformat(event.message.timestamp)
        command = UpdateCommodities(self.commodity_repository, self.market_repository)
        command.execute(
            AddCommodityRequest(
                market_id=event.message.marketId,
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
            commodity_event = from_dict(
                data_class=CommoditiesEvent,
                data=event,
                config=Config(strict=False, convert_key=fix_schema_ref),
            )
            self.event_bus.commodities.publish(commodity_event)


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
