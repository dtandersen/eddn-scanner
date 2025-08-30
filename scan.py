import locale
import logging
import asyncio
import os
import sys

from dotenv import load_dotenv
import psycopg

from scanner.event.eddb_handler import CommodityController
from scanner.event.event_handler import EventBus, MessageHandler
from scanner.event.power_controller import PowerController
from scanner.repo.commodity_repository import PsycopgCommodityRepository
from scanner.repo.market_repository import PsycopgMarketRepository
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import PsycopgSystemRepository
from scanner.scanner import EddnScanner


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
    _writer = CommodityController(
        bus,
        PsycopgCommodityRepository(connection),
        PsycopgMarketRepository(connection),
        PsycopgSystemRepository(connection),
    )
    _power_controller = PowerController(
        bus, PsycopgSystemRepository(connection), PsycopgPowerRepository(connection)
    )
    message_handler = MessageHandler(bus)
    scanner = EddnScanner(message_handler)

    await scanner.start()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
