import zmq
import zmq.asyncio
from dacite import Config
from psycopg.errors import InFailedSqlTransaction

import logging
import zlib

from scanner.event.event_handler import MessageHandler


class EddnScanner:
    """https://pyzmq.readthedocs.io/en/latest/api/zmq.asyncio.html"""

    def __init__(
        self,
        # event_handler: EddnHandler,
        message_handler: MessageHandler,
        endpoint: str = "tcp://eddn.edcd.io:9500",
        timeout: int = 600000,
    ):
        # self._event_handler = event_handler
        self._message_handler = message_handler
        self._endpoint = endpoint
        self._timeout = timeout
        self._log = logging.getLogger(__name__)
        self._config = Config(strict=True)

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
            # self._event_handler.handle(json.loads(msg))
            self._message_handler.process_message(msg.decode("utf-8"))
        except InFailedSqlTransaction as e2:
            raise e2
        except Exception as e:
            self._log.warning(f"Error processing event: {msg}")
            self._log.exception(e)
            # sys.stdout.flush()

    # def _commodity_handler(self, json_msg: Dict[str, Any]):
    #     commodity = from_dict(CommoditiesEvent, json_msg, self._config)
    #     for handler in self._commodities:
    #         handler.on_event(commodity)

    # def _docking_handler(self, json_msg: Dict[str, Any]):
    #     docking = from_dict(DockingEvent, json_msg, self._config)
    #     for handler in self._docking:
    #         handler.on_event(docking)

    # def _signal_handler(self, json_msg: Dict[str, Any]):
    #     signal = from_dict(SignalDiscoveredEvent, json_msg, self._config)
    #     for handler in self._signals:
    #         handler.on_event(signal)

    # def _null_handler(self, _json_msg: Dict[str, Any]):
    #     pass

    # def _unknown_schema_handler(self, json_msg: Dict[str, Any]):
    #     pretty = json.dumps(json_msg, indent=2)
    #     print(pretty)

    # def add_commodity_handler(self, handler: EventHandler[CommoditiesEvent]):
    #     self._commodities.append(handler)

    # def add_docking_handler(self, handler: DockingHandler):
    #     # self.handler = handler
    #     self._docking.append(handler)

    # def add_signal_handler(self, handler: EventHandler[SignalDiscoveredEvent]):
    #     self._signals.append(handler)


# def schema_key(key: str) -> str:
#     return key
