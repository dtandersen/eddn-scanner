import json
import logging
from typing import Callable, Final, Generic, List, TypeVar

from dacite import from_dict

from scanner.event.commodity import CommoditiesEvent
from scanner.event.discovery import DiscoveryEvent
from scanner.event.fsd_jump import FSDJumpEvent


T = TypeVar("T")


class CapturingDelegate(Generic[T]):
    def __init__(self):
        self.events: List[T] = []

    def on_event(self, event: T):
        """Capture the event for later processing."""
        self.events.append(event)


class Delegates(Generic[T]):
    def __init__(self):
        self._listeners: List[Callable[[T], None]] = []

    def add_delegate(self, callback: Callable[[T], None]):
        self._listeners.append(callback)

    def publish(self, event: T):
        for listener in self._listeners:
            listener(event)

    def __iadd__(self, callback: Callable[[T], None]):
        self.add_delegate(callback)
        return self


class EventBus:
    def __init__(self):
        self.commodities: Final = Delegates[CommoditiesEvent]()
        self.discovery: Final = Delegates[DiscoveryEvent]()
        self.fsd_jump: Final = Delegates[FSDJumpEvent]()


class MessageHandler:
    def __init__(self, event_bus: EventBus):
        self._log = logging.getLogger(__name__)
        self._event_bus = event_bus

    def process_message(self, message: str):
        json_msg = json.loads(message)
        event_type = json_msg.get("message", {}).get("event")
        if event_type == "FSDJump":
            msg = from_dict(FSDJumpEvent, json_msg)
            self._event_bus.fsd_jump.publish(msg)
