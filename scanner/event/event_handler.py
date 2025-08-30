import json
import logging
from typing import Callable, Final, Generic, List, TypeVar

from dacite import Config, from_dict

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
        self._listeners: Final[List[Callable[[T], None]]] = []

    def subscribe(self, callback: Callable[[T], None]):
        self._listeners.append(callback)

    def publish(self, event: T):
        for listener in self._listeners:
            listener(event)

    def __iadd__(self, callback: Callable[[T], None]):
        self.subscribe(callback)
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
        event = json_msg
        schema = event.get("$schemaRef")
        if schema == "https://eddn.edcd.io/schemas/commodity/3":
            discovery_event = from_dict(
                data_class=CommoditiesEvent,
                data=event,
                config=Config(strict=False, convert_key=fix_schema_ref),
            )
            self._event_bus.commodities.publish(discovery_event)
        elif schema == "https://eddn.edcd.io/schemas/fssdiscoveryscan/1":
            discovery_event = from_dict(
                data_class=DiscoveryEvent,
                data=event,
                config=Config(strict=False, convert_key=fix_schema_ref),
            )
            self._event_bus.discovery.publish(discovery_event)
        elif schema == "https://eddn.edcd.io/schemas/journal/1":
            event_type = json_msg.get("message", {}).get("event")
            if event_type == "FSDJump":
                msg = from_dict(FSDJumpEvent, json_msg)
                self._event_bus.fsd_jump.publish(msg)


def fix_schema_ref(key: str) -> str:
    if key == "schemaRef":
        return "$schemaRef"
    else:
        return key
