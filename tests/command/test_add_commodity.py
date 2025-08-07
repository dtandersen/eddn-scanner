from datetime import datetime
from hamcrest import assert_that, equal_to
import pytest
from scanner.command.add_commodity import AddCommodity, AddCommodityRequest

from scanner.entity.commodity import Commodity
from scanner.repo.commodity_repository import InMemoryCommodityRepository


@pytest.fixture
def commodity_repository():
    return InMemoryCommodityRepository()


@pytest.fixture
def command(commodity_repository: InMemoryCommodityRepository):
    return AddCommodity(commodity_repository)


def test_commodity_is_added(
    command: AddCommodity, commodity_repository: InMemoryCommodityRepository
):
    timestamp = datetime.now()
    request = AddCommodityRequest(
        commodities=[
            Commodity(
                timestamp=timestamp,
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
                station="station",
                system="system",
            )
        ]
    )
    command.execute(request)

    assert_that(
        commodity_repository.all(),
        equal_to(
            [
                Commodity(
                    timestamp=timestamp,
                    name="gold",
                    buy=90,
                    sell=110,
                    supply=1000,
                    demand=500,
                    station="station",
                    system="system",
                )
            ]
        ),
    )


def test_multiple_commodities_added(
    command: AddCommodity, commodity_repository: InMemoryCommodityRepository
):
    request = AddCommodityRequest(
        commodities=[
            Commodity(
                timestamp=datetime.now(),
                name="gold",
                buy=90,
                sell=110,
                supply=1000,
                demand=500,
                station="station",
                system="system",
            ),
            Commodity(
                timestamp=datetime.now(),
                name="silver",
                buy=50,
                sell=60,
                supply=2000,
                demand=1000,
                station="station2",
                system="system2",
            ),
        ]
    )
    command.execute(request)

    assert_that(
        commodity_repository.all(),
        equal_to(
            [
                Commodity(
                    timestamp=datetime.now(),
                    name="gold",
                    buy=90,
                    sell=110,
                    supply=1000,
                    demand=500,
                    station="station",
                    system="system",
                ),
                Commodity(
                    timestamp=datetime.now(),
                    name="silver",
                    buy=50,
                    sell=60,
                    supply=2000,
                    demand=1000,
                    station="station2",
                    system="system2",
                ),
            ]
        ),
    )
