from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class EventHandler(Generic[T]):
    @abstractmethod
    def on_event(self, event: T):
        pass


@dataclass
class EddnHeader:
    uploaderID: str
    softwareName: str
    softwareVersion: str
    gameversion: Optional[str] = None
    gamebuild: Optional[str] = None
    gatewayTimestamp: Optional[str] = None


@dataclass
class EddnEvent:
    schemaRef: str
    header: EddnHeader
