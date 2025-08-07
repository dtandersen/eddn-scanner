from scanner.event.commodity import CommoditiesEvent
from scanner.event.docking import DockingEvent, DockingHandler
from scanner.event.eddb_handler import EddnHandler
from scanner.event.event import EventHandler
from scanner.event.signals import SignalDiscoveredEvent


import zmq
import zmq.asyncio
from dacite import Config, from_dict


import json
import logging
import zlib
from typing import Any, Callable, Dict, List


class EddnScannerV2:
    """https://pyzmq.readthedocs.io/en/latest/api/zmq.asyncio.html"""

    def __init__(
        self,
        event_handler: EddnHandler,
        endpoint: str = "tcp://eddn.edcd.io:9500",
        timeout: int = 600000,
    ):
        self._event_handler = event_handler
        self._endpoint = endpoint
        self._timeout = timeout
        self._commodities: List[EventHandler[CommoditiesEvent]] = []
        self._docking: List[EventHandler[DockingEvent]] = []
        self._signals: List[EventHandler[SignalDiscoveredEvent]] = []
        self._log = logging.getLogger(__name__)
        self._config = Config(strict=True)
        self._schema_handlers: Dict[str, Callable[[Dict[str, Any]], None]] = {
            "https://eddn.edcd.io/schemas/approachsettlement/1": self._null_handler,
            "https://eddn.edcd.io/schemas/codexentry/1": self._null_handler,
            "https://eddn.edcd.io/schemas/commodity/3": self._commodity_handler,
            "https://eddn.edcd.io/schemas/dockingdenied/1": self._null_handler,
            "https://eddn.edcd.io/schemas/dockinggranted/1": self._docking_handler,
            "https://eddn.edcd.io/schemas/fcmaterials_capi/1": self._null_handler,
            "https://eddn.edcd.io/schemas/fcmaterials_journal/1": self._null_handler,
            "https://eddn.edcd.io/schemas/fssallbodiesfound/1": self._null_handler,
            "https://eddn.edcd.io/schemas/fssbodysignals/1": self._null_handler,
            "https://eddn.edcd.io/schemas/fssdiscoveryscan/1": self._null_handler,
            "https://eddn.edcd.io/schemas/fsssignaldiscovered/1": self._signal_handler,
            "https://eddn.edcd.io/schemas/journal/1": self._null_handler,
            "https://eddn.edcd.io/schemas/navbeaconscan/1": self._null_handler,
            "https://eddn.edcd.io/schemas/navroute/1": self._null_handler,
            "https://eddn.edcd.io/schemas/outfitting/2": self._null_handler,
            "https://eddn.edcd.io/schemas/scanbarycentre/1": self._null_handler,
            "https://eddn.edcd.io/schemas/shipyard/2": self._null_handler,
        }

    async def start(self):
        context = zmq.asyncio.Context()
        sock = context.socket(zmq.SUB)

        sock.setsockopt(zmq.SUBSCRIBE, b"")
        sock.setsockopt(zmq.RCVTIMEO, self._timeout)

        try:
            sock.connect(self._endpoint)

            while True:
                msg = await sock.recv()

                if not msg:
                    self._log.warning("No message received, disconnecting...")
                    # sock.disconnect(self._endpoint)
                    break

                msg = zlib.decompress(msg)
                await self.process_event(msg)

        except zmq.ZMQError as e:
            self._log.exception(f"ZMQ error: {e}")
            # sys.stdout.flush()
            # sock.disconnect(self._endpoint)
        finally:
            self._log.info("Disconnecting from EDDN...")
            sock.disconnect(self._endpoint)

    async def process_event(self, msg: bytes):
        try:
            self._event_handler.handle(json.loads(msg))
            # json_msg = json.loads(msg)
            # self._event_handler.handle(json_msg)
            # pretty = json.dumps(json_msg, indent=2)
            # self._log.debug(f"{pretty}")
            # schema = json_msg.get("$schemaRef")
            # # self._log.info(f"Received message with schema: {schema}")
            # json_msg["schemaRef"] = schema
            # del json_msg["$schemaRef"]

            # if schema is None:
            #     self._log.warning(f"No schemaRef found in message: {json_msg}")
            #     return

            # handler = self._schema_handlers.get(schema)
            # if handler is None:
            #     self._unknown_schema_handler(json_msg)
            #     return

            # handler(json_msg)
        except Exception as e:
            self._log.warning(f"Error processing event: {msg}")
            self._log.exception(e)
            # sys.stdout.flush()

    def _commodity_handler(self, json_msg: Dict[str, Any]):
        commodity = from_dict(CommoditiesEvent, json_msg, self._config)
        for handler in self._commodities:
            handler.on_event(commodity)

    def _docking_handler(self, json_msg: Dict[str, Any]):
        docking = from_dict(DockingEvent, json_msg, self._config)
        for handler in self._docking:
            handler.on_event(docking)

    def _signal_handler(self, json_msg: Dict[str, Any]):
        signal = from_dict(SignalDiscoveredEvent, json_msg, self._config)
        for handler in self._signals:
            handler.on_event(signal)

    def _null_handler(self, _json_msg: Dict[str, Any]):
        pass

    def _unknown_schema_handler(self, json_msg: Dict[str, Any]):
        pretty = json.dumps(json_msg, indent=2)
        print(pretty)

    def add_commodity_handler(self, handler: EventHandler[CommoditiesEvent]):
        self._commodities.append(handler)

    def add_docking_handler(self, handler: DockingHandler):
        # self.handler = handler
        self._docking.append(handler)

    def add_signal_handler(self, handler: EventHandler[SignalDiscoveredEvent]):
        self._signals.append(handler)


def schema_key(key: str) -> str:
    return key
