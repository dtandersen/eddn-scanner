from datetime import datetime
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
                        distance=0,
                    )
                ]
            )
        ),
    )


def test_returns_markets_within_10ly(
    command_factory: CommandFactory,
    test_facade: TestFacade,
):
    test_facade.given_system(1, "System 1", Point3D(0, 0, 0))
    test_facade.given_system(2, "System 2", Point3D(10, 0, 0))
    test_facade.given_system(3, "System 2", Point3D(0, 0, 11))
    test_facade.given_market(1, 1, "Market 1")
    test_facade.given_market(2, 2, "Market 2")
    test_facade.given_market(3, 3, "Market 3")

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
                        distance=10.0,
                        power_state=None,
                        power=None,
                    ),
                    MarketDto(
                        market_id=1,
                        system_address=1,
                        market_name="Market 1",
                        system_name="System 1",
                        landing_pad="?",
                        distance=0.0,
                        power_state=None,
                        power=None,
                    ),
                ]
            )
        ),
    )


def test_returns_markets_within_10ly_power_state(
    command_factory: CommandFactory,
    test_facade: TestFacade,
):
    test_facade.given_system(1, "System 1", Point3D(0, 0, 0))
    test_facade.given_system(2, "System 2", Point3D(10, 0, 0))
    test_facade.given_system(3, "System 2", Point3D(0, 0, 11))

    test_facade.given_system_state(1, "Stronghold", "Yuri Grom", datetime.now())
    test_facade.given_system_state(2, "Fortified", "Yuri Grom", datetime.now())
    test_facade.given_system_state(3, "Exploited", "Yuri Grom", datetime.now())

    test_facade.given_market(1, 1, "Market 1")
    test_facade.given_market(2, 2, "Market 2")
    test_facade.given_market(3, 3, "Market 3")

    request = ListMarketsRequest(
        system=1, distance=30, power_state=["Fortified", "Stronghold"]
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
                        distance=0.0,
                        power_state="Stronghold",
                        power="Yuri Grom",
                    ),
                    MarketDto(
                        market_id=2,
                        system_address=2,
                        market_name="Market 2",
                        system_name="System 2",
                        landing_pad="?",
                        distance=10.0,
                        power_state="Fortified",
                        power="Yuri Grom",
                    ),
                ]
            )
        ),
    )
