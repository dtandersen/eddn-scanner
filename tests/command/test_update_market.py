import pytest

from scanner.command.update_market import UpdateMarket, UpdateMarketRequest
from scanner.repo.commodity_repository import (
    PsycopgCommodityRepository,
)
from scanner.repo.market_repository import PsycopgMarketRepository
from scanner.repo.system_repository import SystemRepository
from tests.facade import TestFacade


@pytest.fixture
def command(
    market_repository: PsycopgMarketRepository,
    system_repository: SystemRepository,
):
    return UpdateMarket(market_repository, system_repository)


def test_commodity_is_added(
    command: UpdateMarket,
    commodity_repository: PsycopgCommodityRepository,
    test_facade: TestFacade,
):
    request = UpdateMarketRequest(
        market_id=1,
    )
    command.execute(request)
