import locale
import logging
import asyncio
import sys

from scanner.event.eddb_handler import LoggingEddnHandler
from scanner.scanner2 import EddnScannerV2


async def main():
    locale.setlocale(locale.LC_ALL, "")
    file_handler = logging.FileHandler("scanner.log")
    # file_handler.addFilter(DuplicateFilter())
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    # stream_handler.addFilter(DuplicateFilter())

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)7s  %(message)s",
        datefmt="%H:%M:%S",
        # format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        handlers=[file_handler, stream_handler],
    )

    scanner = EddnScannerV2(
        LoggingEddnHandler(
            None
            # [
            #     # "https://eddn.edcd.io/schemas/commodity/3",
            #     # "https://eddn.edcd.io/schemas/fssdiscoveryscan/1",
            # ]
        )
    )
    # scanner.add_docking_handler(DockingHandler())
    # scanner.add_signal_handler(SignalDiscoveredHandler())
    # scanner.add_commodity_handler(CommodityHandler())

    await scanner.start()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
