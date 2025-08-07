from hamcrest import assert_that, equal_to
import pytest
from scanner.command.add_commodity import AddCommodity, AddCommodityRequest

from scanner.entity.commodity import Commodity
from scanner.entity.system import Point3D
from scanner.repo.commodity_repository import (
    InMemoryCommodityRepository,
    PsycopgCommodityRepository,
)
from tests.facade import Facade


@pytest.fixture
def command(commodity_repository: PsycopgCommodityRepository):
    return AddCommodity(commodity_repository)


def test_commodity_is_added(
    command: AddCommodity,
    commodity_repository: PsycopgCommodityRepository,
    facade: Facade,
):
    facade.given_system(address=1, name="Test System", position=Point3D(0, 0, 0))
    facade.given_market(
        market_id=1, system_address=1, name="Test Station", last_updated=None
    )
    # _timestamp = datetime.now()
    request = AddCommodityRequest(
        commodities=[
            Commodity(
                market_id=1,
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
            )
        ]
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
    command: AddCommodity,
    commodity_repository: InMemoryCommodityRepository,
    facade: Facade,
):
    facade.given_system(address=1, name="Test System", position=Point3D(0, 0, 0))
    facade.given_market(
        market_id=1, system_address=1, name="Test Station", last_updated=None
    )

    request = AddCommodityRequest(
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
        ]
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
