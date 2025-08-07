from dataclasses import dataclass
import logging

from scanner.event.event import EddnEvent, EventHandler


@dataclass
class DockingMessage:
    LandingPad: int
    MarketID: int
    StationName: str
    StationType: str
    event: str
    horizons: bool
    odyssey: bool
    timestamp: str


@dataclass
class DockingEvent(EddnEvent):
    message: DockingMessage


class DockingHandler(EventHandler[DockingEvent]):
    def __init__(self):
        self._log = logging.getLogger(__name__)

    def on_event(self, event: DockingEvent):
        if event.message.StationType != "FleetCarrier":
            return

        # self._log.info(
        #     f"Docked at {event.message.StationName} on pad {event.message.LandingPad}"
        # )
