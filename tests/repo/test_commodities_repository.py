from hamcrest import assert_that, equal_to
from scanner.entity.commodity import Commodity
from scanner.entity.market import Market
from scanner.entity.system import Point3D, System
from scanner.repo.commodity_repository import PsycopgCommodityRepository
from scanner.repo.market_repository import PsycopgMarketRepository
from scanner.repo.system_repository import PsycopgSystemRepository

# import pytest

# postgres = PostgresContainer("postgres:16-alpine")


# def get_connection():
#     host = os.getenv("DB_HOST", "localhost")
#     port = os.getenv("DB_PORT", "5432")
#     username = os.getenv("DB_USERNAME", "postgres")
#     password = os.getenv("DB_PASSWORD", "postgres")
#     database = os.getenv("DB_NAME", "scanner-dev")

#     return psycopg.connect(
#         f"host={host} dbname={database} user={username} password={password} port={port}"
#     )


# @pytest.fixture(scope="session", autouse=True)
# def setup(request: pytest.FixtureRequest):
#     postgres.start()

#     def remove_container():
#         postgres.stop()

#     request.addfinalizer(remove_container)
#     os.environ["DB_CONN"] = postgres.get_connection_url()
#     os.environ["DB_HOST"] = postgres.get_container_host_ip()
#     os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
#     os.environ["DB_USERNAME"] = postgres.username
#     os.environ["DB_PASSWORD"] = postgres.password
#     os.environ["DB_NAME"] = postgres.dbname
#     # customers.create_table()


# @pytest.fixture
# def commodity_repository(connection: psycopg.Connection):
#     return PsycogCommodityRepository(connection)


# @pytest.fixture
# def system_repository(connection: psycopg.Connection):
#     return PsycopgSystemRepository(connection)


# @pytest.fixture
# def market_repository(connection: psycopg.Connection):
#     return PsycopgMarketRepository(connection)


# @pytest.mark.slow
def test_creates_commodity_in_repository(
    commodity_repository: PsycopgCommodityRepository,
    system_repository: PsycopgSystemRepository,
    market_repository: PsycopgMarketRepository,
):
    system_repository.create(
        System(address=1, name="system", position=Point3D(0, 0, 0))
    )
    market_repository.create(
        Market(system_address=1, market_id=1, name="station", last_updated=None)
    )

    commodity = Commodity(
        market_id=1,
        name="gold",
        buy=90,
        sell=110,
        supply=1000,
        demand=500,
    )
    commodity_repository.create(commodity)

    assert_that(
        commodity_repository.all(),
        equal_to([commodity]),
    )
