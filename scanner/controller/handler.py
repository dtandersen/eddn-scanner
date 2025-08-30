from abc import ABCMeta, abstractmethod
from typing import Any, Dict


import json
import logging

EddnEvent = Dict[str, Any]


class EddnHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, event: EddnEvent):
        pass


class LoggingEddnHandler(EddnHandler):
    log = logging.getLogger(__name__)

    def __init__(self, filter: list[str] | None = None):
        self.filter = filter

    def handle(self, event: EddnEvent):
        schema = event.get("$schemaRef")
        if self.filter and schema not in self.filter:
            return

        self.log.info(f"{json.dumps(event, indent=2)}\n---")
