from datetime import datetime, timezone
from hamcrest import assert_that, equal_to
import psycopg
import pytest
from yoyo import get_backend, read_migrations  # type: ignore
from scanner.entity.commodity import Commodity
from scanner.repo.commodity_repository import PsycogCommodityRepository
import os
from testcontainers.postgres import PostgresContainer  # type: ignore

# import pytest

postgres = PostgresContainer("postgres:16-alpine")


def get_connection():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    username = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    database = os.getenv("DB_NAME", "scanner-dev")

    return psycopg.connect(
        f"host={host} dbname={database} user={username} password={password} port={port}"
    )


@pytest.fixture(scope="session", autouse=True)
def setup(request: pytest.FixtureRequest):
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
    # customers.create_table()


@pytest.fixture
def commodity_repository():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    username = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    database = os.getenv("DB_NAME", "postgres")
    backend = get_backend(
        f"postgresql+psycopg://{username}:{password}@{host}:{port}/{database}"
    )
    migrations = read_migrations("migrations")

    with backend.lock():

        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))

        # Rollback all migrations
        backend.rollback_migrations(backend.to_rollback(migrations))
    return PsycogCommodityRepository(get_connection())


@pytest.mark.slow
def test_creates_commodity_in_repository(
    commodity_repository: PsycogCommodityRepository,
):
    timestamp = datetime(2025, 8, 6, 22, 53, 24, 648057, tzinfo=timezone.utc)
    commodity = Commodity(
        timestamp=timestamp,
        name="gold",
        buy=90,
        sell=110,
        supply=1000,
        demand=500,
        station="station",
        system="system",
    )
    commodity_repository.create(commodity)

    assert_that(
        commodity_repository.all(),
        equal_to([commodity]),
    )
