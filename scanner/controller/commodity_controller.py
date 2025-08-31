from datetime import datetime
import logging


# from scanner import scanner
from scanner.command.command_factory import CommandFactory
from scanner.command.update_commodities import UpdateCommoditiesRequest
from scanner.entity.commodity import Commodity
from scanner.event.commodity import CommoditiesEvent, CommodityEvent
from scanner.event.event_handler import EventBus


class CommodityController:
    log = logging.getLogger(__name__)

    def __init__(
        self,
        events: EventBus,
        command_factory: CommandFactory,
    ):
        events.commodities.subscribe(self.on_commodities)
        # events.discovery.subscribe(self.on_discovery)

        self.command_factory = command_factory

    def on_commodities(self, event: CommoditiesEvent):
        timestamp = datetime.fromisoformat(event.message.timestamp)
        command = self.command_factory.update_commodities()
        command.execute(
            UpdateCommoditiesRequest(
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

    # def on_discovery(self, event: DiscoveryEvent):
    #     command = self.command_factory.update_system()
    #     command.execute(
    #         UpdateSystemRequest(
    #             system_address=event.message.SystemAddress,
    #             system_name=event.message.SystemName,
    #             position=Point3D(
    #                 event.message.StarPos[0],
    #                 event.message.StarPos[1],
    #                 event.message.StarPos[2],
    #             ),
    #             state=None,
    #             powers=[],
    #         )
    #     )

    def map_to_commodity(self, event: CommodityEvent, market_id: int) -> Commodity:
        return Commodity(
            market_id=market_id,
            name=event.name,
            buy=event.buyPrice,
            sell=event.sellPrice,
            supply=event.stock,
            demand=event.demand,
        )
