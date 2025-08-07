from datetime import datetime, timezone
from hamcrest import assert_that, equal_to
import pytest
from scanner.command.update_commodities import UpdateCommodities, AddCommodityRequest

from scanner.entity.commodity import Commodity
from scanner.entity.system import Point3D
from scanner.repo.commodity_repository import (
    PsycopgCommodityRepository,
)
from scanner.repo.market_repository import PsycopgMarketRepository
from tests.facade import TestFacade


@pytest.fixture
def command(
    commodity_repository: PsycopgCommodityRepository,
    market_repository: PsycopgMarketRepository,
):
    return UpdateCommodities(commodity_repository, market_repository)


def test_commodity_is_added(
    command: UpdateCommodities,
    commodity_repository: PsycopgCommodityRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="Test System", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1, system_address=1, name="Test Station", last_updated=None
    )
    timestamp = datetime.now()
    request = AddCommodityRequest(
        market_id=1,
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
    command.execute(request)

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
    command: UpdateCommodities,
    commodity_repository: PsycopgCommodityRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="Test System", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1, system_address=1, name="Test Station", last_updated=None
    )

    timestamp = datetime.now()
    request = AddCommodityRequest(
        market_id=1,
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
    command.execute(request)

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
    command: UpdateCommodities,
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
    request = AddCommodityRequest(
        market_id=1,
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
    command.execute(request)

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


def test_dont_add_commodities_if_market_doesnt_exist(
    command: UpdateCommodities,
    commodity_repository: PsycopgCommodityRepository,
):

    timestamp = datetime.now()
    request = AddCommodityRequest(
        market_id=1,
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
    command.execute(request)

    assert_that(
        commodity_repository.all(),
        equal_to([]),
    )
