import locale
import logging
import asyncio
import os

from dotenv import load_dotenv
import psycopg

from scanner.event.eddb_handler import CommodityEddnHandler, CommodityWriter
from scanner.event.event_handler import EventBus
from scanner.repo.commodity_repository import PsycopgCommodityRepository
from scanner.repo.market_repository import PsycopgMarketRepository
from scanner.scanner2 import EddnScannerV2


def get_connection():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    username = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    database = os.getenv("DB_NAME", "scanner-dev")

    return psycopg.connect(
        f"host={host} dbname={database} user={username} password={password} port={port}"
    )


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
    load_dotenv()
    bus = EventBus()
    connection = get_connection()
    _writer = CommodityWriter(
        bus, PsycopgCommodityRepository(connection), PsycopgMarketRepository(connection)
    )
    scanner = EddnScannerV2(CommodityEddnHandler(bus))
    # scanner.add_docking_handler(DockingHandler())
    # scanner.add_signal_handler(SignalDiscoveredHandler())
    # scanner.add_commodity_handler(CommodityHandler())

    await scanner.start()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
