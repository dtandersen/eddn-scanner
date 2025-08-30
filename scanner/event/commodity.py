from scanner.event.event import EddnEvent


from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class CommodityEvent:
    name: str
    meanPrice: int
    buyPrice: int
    stock: int
    stockBracket: Union[int, str]
    sellPrice: int
    demand: int
    demandBracket: Union[int, str]
    statusFlags: Optional[List[str]] = None


@dataclass
class Economy:
    name: str
    proportion: float


@dataclass
class CommodityMessage:
    systemName: str
    stationName: str
    marketId: int
    timestamp: str
    commodities: List[CommodityEvent]
    stationType: Optional[str] = None
    # none, squadronfriends, friends, squadron, all
    carrierDockingAccess: Optional[str] = None
    horizons: Optional[bool] = None
    odyssey: Optional[bool] = None
    economies: Optional[List[Economy]] = None
    prohibited: Optional[List[str]] = None


@dataclass
class CommoditiesEvent(EddnEvent):
    message: CommodityMessage


# class CommodityHandler(EventHandler[CommoditiesEvent]):
#     def __init__(self):
#         self._log = logging.getLogger(__name__)

#     def on_event(self, event: CommoditiesEvent):
#         if event.message.carrierDockingAccess is None:
#             return

#         if event.message.carrierDockingAccess in [
#             "none",
#             "squadron",
#             "squadronfriends",
#             "friends",
#         ]:
#             return

#         ban_list = ["thargoidtitandrivecomponent"]
#         buying_commodities = [
#             commodity
#             for commodity in event.message.commodities
#             if commodity.sellPrice > 0
#             and commodity.demand > 0
#             and commodity.name not in ban_list
#         ]
#         if len(buying_commodities) == 0:
#             # self._log.info("No commodities available for sale.")
#             return

#         self._log.info(
#             f"Received commodity data for {event.message.stationName} in {event.message.systemName} [docking={event.message.carrierDockingAccess}]"
#         )

#         self._log.info("Commodity                                 Sell     Demand")
#         self._log.info("------------------------------ --------------- ----------")

#         for commodity in buying_commodities:
#             self._log.info(
#                 f"{commodity.name:<30} {commodity.sellPrice:12n} Cr {commodity.demand:10n}"
#             )
