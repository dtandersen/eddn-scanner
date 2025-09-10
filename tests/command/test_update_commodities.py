from datetime import datetime, timezone
from hamcrest import assert_that, equal_to
import pytest
from scanner.command.update_commodities import (
    UpdateMarketCommoditiesHandler,
    UpdateCommodities,
)

from scanner.entity.commodity import Commodity
from scanner.entity.market import Market
from scanner.entity.system import Point3D
from scanner.repo.commodity_repository import (
    PsycopgCommodityRepository,
)
from scanner.repo.market_repository import PsycopgMarketRepository
from scanner.repo.system_repository import SystemRepository
from tests.facade import TestFacade


@pytest.fixture
def command(
    commodity_repository: PsycopgCommodityRepository,
    market_repository: PsycopgMarketRepository,
    system_repository: SystemRepository,
):
    return UpdateMarketCommoditiesHandler(
        commodity_repository, market_repository, system_repository
    )


def test_commodity_is_added(
    command: UpdateMarketCommoditiesHandler,
    commodity_repository: PsycopgCommodityRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="Test System", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1, system_address=1, name="Test Station", last_updated=None
    )
    timestamp = datetime.now()
    request = UpdateCommodities(
        market_id=1,
        station="Test Station",
        system="Test System",
        timestamp=timestamp,
        commodities=[
            Commodity(
                market_id=1,
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
            )
        ],
    )
    command.handle(request)

    assert_that(
        commodity_repository.all(),
        equal_to(
            [
                Commodity(
                    market_id=1,
                    name="gold",
                    buy=90,
                    sell=110,
                    supply=1000,
                    demand=500,
                )
            ]
        ),
    )


def test_multiple_commodities_added(
    command: UpdateMarketCommoditiesHandler,
    commodity_repository: PsycopgCommodityRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="Test System", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1, system_address=1, name="Test Station", last_updated=None
    )

    timestamp = datetime.now()
    request = UpdateCommodities(
        market_id=1,
        station="Test Station",
        system="Test System",
        timestamp=timestamp,
        commodities=[
            Commodity(
                market_id=1,
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
            ),
            Commodity(
                market_id=1,
                name="silver",
                buy=50,
                sell=60,
                supply=2000,
                demand=1000,
            ),
        ],
    )
    command.handle(request)

    assert_that(
        commodity_repository.all(),
        equal_to(
            [
                Commodity(
                    market_id=1,
                    name="gold",
                    buy=90,
                    sell=110,
                    supply=1000,
                    demand=500,
                ),
                Commodity(
                    market_id=1,
                    name="silver",
                    buy=50,
                    sell=60,
                    supply=2000,
                    demand=1000,
                ),
            ]
        ),
    )


def test_previous_market_prices_are_overwritten(
    command: UpdateMarketCommoditiesHandler,
    commodity_repository: PsycopgCommodityRepository,
    market_repository: PsycopgMarketRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="Test System", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1, system_address=1, name="Test Station", last_updated=None
    )
    test_facade.given_commodity(
        market_id=1,
        name="gold",
    )

    timestamp = datetime.now(tz=timezone.utc)
    request = UpdateCommodities(
        market_id=1,
        station="Test Station",
        system="Test System",
        timestamp=timestamp,
        commodities=[
            Commodity(
                market_id=1,
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
            ),
        ],
    )
    command.handle(request)

    assert_that(
        commodity_repository.all(),
        equal_to(
            [
                Commodity(
                    market_id=1,
                    name="gold",
                    buy=90,
                    sell=110,
                    supply=1000,
                    demand=500,
                ),
            ]
        ),
    )

    market = market_repository.get_market(1)
    assert_that(market.last_updated, equal_to(timestamp))


def test_add_market_if_system_exists(
    command: UpdateMarketCommoditiesHandler,
    commodity_repository: PsycopgCommodityRepository,
    market_repository: PsycopgMarketRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="System", position=Point3D(0, 0, 0))

    timestamp = datetime.now(tz=timezone.utc)
    request = UpdateCommodities(
        market_id=1,
        station="ABC-123",
        system="System",
        station_type="FleetCarrier",
        docking_access="all",
        timestamp=timestamp,
        commodities=[
            Commodity(
                market_id=1,
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
            ),
        ],
    )
    command.handle(request)

    assert_that(
        market_repository.all(),
        equal_to(
            [
                Market(
                    market_id=1,
                    system_address=1,
                    name="ABC-123",
                    station_type="FleetCarrier",
                    docking_access="all",
                    last_updated=timestamp,
                ),
            ]
        ),
    )

    assert_that(
        commodity_repository.all(),
        equal_to(
            [
                Commodity(
                    market_id=1,
                    name="gold",
                    buy=90,
                    sell=110,
                    supply=1000,
                    demand=500,
                ),
            ]
        ),
    )

    assert_that(
        commodity_repository.all(),
        equal_to(
            [
                Commodity(
                    market_id=1,
                    name="gold",
                    buy=90,
                    sell=110,
                    supply=1000,
                    demand=500,
                ),
            ]
        ),
    )


def test_dont_add_commodities_if_market_doesnt_exist(
    command: UpdateMarketCommoditiesHandler,
    commodity_repository: PsycopgCommodityRepository,
):
    timestamp = datetime.now()
    request = UpdateCommodities(
        market_id=1,
        station="Unknown",
        system="Unknown",
        timestamp=timestamp,
        commodities=[
            Commodity(
                market_id=1,
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
            ),
        ],
    )
    command.handle(request)

    assert_that(
        commodity_repository.all(),
        equal_to([]),
    )


def test_docking_access_is_updated(
    command: UpdateMarketCommoditiesHandler,
    market_repository: PsycopgMarketRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="System", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1,
        system_address=1,
        name="ABC-123",
        station_type="FleetCarrier",
        docking_access=None,
    )

    timestamp = datetime.now(tz=timezone.utc)
    request = UpdateCommodities(
        market_id=1,
        station="ABC-123",
        system="System",
        station_type="FleetCarrier",
        docking_access="all",
        timestamp=timestamp,
        commodities=[
            Commodity(
                market_id=1,
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
            ),
        ],
    )
    command.handle(request)

    assert_that(
        market_repository.get_market(1),
        equal_to(
            Market(
                market_id=1,
                system_address=1,
                name="ABC-123",
                station_type="FleetCarrier",
                docking_access="all",
                last_updated=timestamp,
            ),
        ),
    )


def test_station_type_is_updated(
    command: UpdateMarketCommoditiesHandler,
    market_repository: PsycopgMarketRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="System", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1,
        system_address=1,
        name="ABC-123",
        station_type=None,
    )

    timestamp = datetime.now(tz=timezone.utc)
    request = UpdateCommodities(
        market_id=1,
        station="ABC-123",
        system="System",
        station_type="FleetCarrier",
        docking_access="all",
        timestamp=timestamp,
        commodities=[
            Commodity(
                market_id=1,
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
            ),
        ],
    )
    command.handle(request)

    assert_that(
        market_repository.get_market(1),
        equal_to(
            Market(
                market_id=1,
                system_address=1,
                name="ABC-123",
                station_type="FleetCarrier",
                docking_access="all",
                last_updated=timestamp,
            ),
        ),
    )
