from typing import Callable, Final, Generic, List, TypeVar

from scanner.event.commodity import CommoditiesEvent


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
