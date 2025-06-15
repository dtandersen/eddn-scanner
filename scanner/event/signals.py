from dataclasses import dataclass
import logging
from typing import List, Optional

from scanner.event.event import EddnEvent, EventHandler


@dataclass
class Signal:
    timestamp: str
    SignalName: str
    IsStation: bool = False
    SignalType: Optional[str] = None
    USSType: Optional[str] = None
    SpawningState: Optional[str] = None
    SpawningFaction: Optional[str] = None
    SpawningPower: Optional[str] = None
    OpposingPower: Optional[str] = None
    ThreatLevel: Optional[int] = None


@dataclass
class SignalMessage:
    event: str
    timestamp: str
    SystemAddress: int
    StarSystem: str
    StarPos: List[float]
    signals: List[Signal]
    horizons: Optional[bool] = None
    odyssey: Optional[bool] = None


@dataclass
class SignalDiscoveredEvent(EddnEvent):
    message: SignalMessage


class SignalDiscoveredHandler(EventHandler[SignalDiscoveredEvent]):
    def __init__(self):
        self._log = logging.getLogger(__name__)
        pass

    def on_event(self, event: SignalDiscoveredEvent):
        # self._log.info(f"Signal discovered in system {event}")
        stations = [signal for signal in event.message.signals if signal.IsStation]
        station_count = len(stations)
        # for signal in event.message.signals:
        #     # self._log.info(
        #     #     f"Station discovered: {signal.SignalName} in system {event.message.StarSystem}, {signal.IsStation=}"
        #     # )
        #     if not signal.IsStation:
        #         return
        if station_count == 0:
            return

        self._log.info(
            f"Discovered {len(stations)} stations in system {event.message.StarSystem}"
        )
        # print(f"Signal discovered: {event.message.SignalName} in system {event.message.StarSystem}")
