import locale
import logging
import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scan import get_connection
from scanner.command.command_factory import CommandFactory
from scanner.command.get_system import GetSystemRequest
from scanner.command.list_systems import ListSystemsRequest
from scanner.event.event_handler import EventBus
from scanner.repo.commodity_repository import PsycopgCommodityRepository
from scanner.repo.market_repository import PsycopgMarketRepository
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import PsycopgSystemRepository


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

locale.setlocale(locale.LC_ALL, "")
load_dotenv()
# config = dotenv_values()
handlers: List[logging.Handler] = []
scanner_log = os.getenv("SCANNER_LOG", "true")
print(f"SCANNER_LOG={scanner_log}")
if scanner_log != "false":
    file_handler = logging.FileHandler("scanner.log")
    # file_handler.addFilter(DuplicateFilter())
    file_handler.setLevel(logging.DEBUG)
    handlers.append(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handlers.append(stream_handler)
# stream_handler.addFilter(DuplicateFilter())

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)7s  %(message)s",
    datefmt="%H:%M:%S",
    # format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=handlers,
)
bus = EventBus()
connection = get_connection()
command_factory = CommandFactory(
    PsycopgSystemRepository(connection),
    PsycopgMarketRepository(connection),
    PsycopgCommodityRepository(connection),
    PsycopgPowerRepository(connection),
)
# _commodity_controller = CommodityController(
#     bus,
#     command_factory,
# )
# _system_controller = SystemController(
#     bus,
#     command_factory,
# )
# message_handler = MessageHandler(bus)
# scanner = EddnScanner(message_handler)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Set to True if your frontend sends cookies or authorization headers
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/systems/{address}")
def get_system(address: int):
    request = GetSystemRequest(system_address=address)
    command = command_factory.get_system()
    system = command.execute(request)
    return system


@app.get("/systems")
def list_systems(name: str):
    request = ListSystemsRequest(name=name)
    command = command_factory.list_systems()
    systems = command.execute(request)
    return systems
