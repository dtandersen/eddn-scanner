from hamcrest import assert_that, equal_to

from scanner.command.command_factory import CommandFactory
from scanner.command.list_markets import ListMarketsRequest, ListMarketsResult
from scanner.dto.market import MarketDto
from scanner.entity.system import Point3D
from scanner.repo.market_repository import MarketRepository
from tests.facade import TestFacade


# @pytest.fixture
# def command(
#     system_repository: SystemRepository, power_repository: PsycopgPowerRepository
# ):
#     return UpdateSystem(system_repository, power_repository)


def test_returns_markets_in_system(
    command_factory: CommandFactory,
    # power_repository: PsycopgPowerRepository,
    market_repository: MarketRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(1, "System 1", Point3D(1, 2, 3))
    # test_facade.given_system(2, "System 2", Point3D(1, 2, 3))
    test_facade.given_market(1, 1, "Market 1")
    # test_facade.given_market(2, "Market 2", "System 2", "Landing Pad 2", 200.0)

    request = ListMarketsRequest(
        system=1,
    )
    command = command_factory.list_markets()
    markets = command.execute(request)

    assert_that(
        markets,
        equal_to(
            ListMarketsResult(
                markets=[
                    MarketDto(
                        market_id=1,
                        system_address=1,
                        market_name="Market 1",
                        system_name="System 1",
                        landing_pad="?",
                    )
                ]
            )
        ),
    )


def test_returns_markets_within_10ly(
    command_factory: CommandFactory,
    # power_repository: PsycopgPowerRepository,
    market_repository: MarketRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(1, "System 1", Point3D(0, 0, 0))
    test_facade.given_system(2, "System 2", Point3D(10, 0, 0))
    test_facade.given_market(1, 1, "Market 1")
    test_facade.given_market(2, 2, "Market 2")
    # test_facade.given_market(2, "Market 2", "System 2", "Landing Pad 2", 200.0)

    request = ListMarketsRequest(system=1, distance=10)
    command = command_factory.list_markets()
    markets = command.execute(request)

    assert_that(
        markets,
        equal_to(
            ListMarketsResult(
                markets=[
                    MarketDto(
                        market_id=2,
                        system_address=2,
                        market_name="Market 2",
                        system_name="System 2",
                        landing_pad="?",
                    )
                ]
            )
        ),
    )
