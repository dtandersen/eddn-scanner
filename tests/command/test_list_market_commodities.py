from hamcrest import assert_that, equal_to
import pytest
from scanner.command.command_factory import CommandFactory
from scanner.command.list_market_commodities import (
    ListMarketCommodities,
    ListMarketCommoditiesHandler,
    ListMarketCommoditiesResult,
)

from scanner.entity.commodity import Commodity
from scanner.entity.system import Point3D
from tests.facade import TestFacade


@pytest.fixture
def handler(command_factory: CommandFactory):
    return command_factory.list_market_commodities()


def test_commodity_is_added(
    handler: ListMarketCommoditiesHandler,
    # commodity_repository: PsycopgCommodityRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="System 1", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1, system_address=1, name="Market 1", last_updated=None
    )
    test_facade.given_commodity(
        market_id=1, name="gold", buy=90, sell=110, supply=1000, demand=500
    )
    test_facade.given_commodity(
        market_id=1, name="silver", buy=90, sell=110, supply=1000, demand=500
    )

    result = handler.handle(ListMarketCommodities(market_id=1))

    assert_that(
        result,
        equal_to(
            ListMarketCommoditiesResult(
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
                        buy=90,
                        sell=110,
                        supply=1000,
                        demand=500,
                    ),
                ]
            )
        ),
    )
