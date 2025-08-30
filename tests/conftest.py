from dataclasses import dataclass
from typing import List
import psycopg
import pytest
from yoyo import get_backend, read_migrations  # type: ignore
import os
from testcontainers.postgres import PostgresContainer  # type: ignore

from scanner.event.event_handler import EventBus, MessageHandler
from scanner.event.power_controller import PowerController
from scanner.repo.commodity_repository import PsycopgCommodityRepository
from scanner.repo.market_repository import PsycopgMarketRepository
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import PsycopgSystemRepository, SystemRepository
from tests.facade import TestFacade  # type: ignore


def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config: pytest.Config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config: pytest.Config, items: List[pytest.Item]):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture(scope="session")
def postgres():
    container = PostgresContainer("postgres:17-alpine")
    return container


@dataclass
class ConnectionConfig:
    host: str
    port: str
    username: str
    password: str
    database: str


@pytest.fixture(scope="session")
def database_config(request: pytest.FixtureRequest, postgres: PostgresContainer):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    os.environ["DB_CONN"] = postgres.get_connection_url()
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USERNAME"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5555")
    username = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    database = os.getenv("DB_NAME", "scanner-dev")

    backend = get_backend(
        f"postgresql+psycopg://{username}:{password}@{host}:{port}/{database}"
    )
    migrations = read_migrations("migrations")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
        backend.rollback_migrations(backend.to_rollback(migrations))

    return ConnectionConfig(
        host=host, port=port, username=username, password=password, database=database
    )


@pytest.fixture()
def connection(
    request: pytest.FixtureRequest, database_config: ConnectionConfig
) -> psycopg.Connection:
    connection = psycopg.connect(
        f"host={database_config.host} dbname={database_config.database} user={database_config.username} password={database_config.password} port={database_config.port}"
    )

    connection.execute("truncate system cascade")
    connection.execute("truncate sys_power cascade")

    def remove_container():
        connection.close()

    request.addfinalizer(remove_container)

    return connection


@pytest.fixture
def commodity_repository(connection: psycopg.Connection):
    return PsycopgCommodityRepository(connection)


@pytest.fixture
def system_repository(connection: psycopg.Connection):
    return PsycopgSystemRepository(connection)


@pytest.fixture
def power_repository(connection: psycopg.Connection):
    return PsycopgPowerRepository(connection)


@pytest.fixture
def market_repository(connection: psycopg.Connection):
    return PsycopgMarketRepository(connection)


@pytest.fixture
def test_facade(
    system_repository: PsycopgSystemRepository,
    market_repository: PsycopgMarketRepository,
    commodity_repository: PsycopgCommodityRepository,
):
    return TestFacade(
        system_repository=system_repository,
        market_repository=market_repository,
        commodity_repository=commodity_repository,
    )


@pytest.fixture
def event_bus():
    return EventBus()


@pytest.fixture
def message_handler(event_bus: EventBus):
    return MessageHandler(event_bus)


@pytest.fixture
def power_controller(
    event_bus: EventBus,
    system_repository: SystemRepository,
    power_repository: PsycopgPowerRepository,
):
    return PowerController(event_bus, system_repository, power_repository)
