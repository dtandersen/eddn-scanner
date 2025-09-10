from hamcrest import assert_that, equal_to
import pytest
from scanner.command.command_factory import CommandFactory

from scanner.command.list_trades import (
    ListTrades,
    ListTradesHandler,
    ListTradesResult,
)
from scanner.dto.trade import Trade
from scanner.entity.system import Point3D
from tests.facade import TestFacade


@pytest.fixture
def handler(command_factory: CommandFactory):
    return command_factory.list_trades()


def test_commodity_is_added2(
    handler: ListTradesHandler,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="Buy System 1", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1, system_address=1, name="Buy Market 1", last_updated=None
    )
    test_facade.given_system(
        address=2, name="Sell System 2", position=Point3D(0, 10, 0)
    )
    test_facade.given_market(
        market_id=2, system_address=2, name="Sell Market 2", last_updated=None
    )
    test_facade.given_commodity(
        market_id=1, name="gold", buy=1000, sell=0, supply=1000, demand=0
    )
    test_facade.given_commodity(
        market_id=2, name="gold", buy=0, sell=2000, supply=0, demand=1000
    )

    result = handler.handle(ListTrades(buy_market=1, sell_market=2))

    assert_that(
        result,
        equal_to(
            ListTradesResult(
                trades=[
                    Trade(
                        buy_market_id=1,
                        buy_market_name="Buy Market 1",
                        sell_market_id=2,
                        sell_market_name="Sell Market 2",
                        commodity="gold",
                        buy=1000,
                        sell=2000,
                        supply=1000,
                        demand=1000,
                        profit=1000,
                        distance=0.0,
                    )
                ]
            )
        ),
    )


def test_commodity_is_added(
    handler: ListTradesHandler,
    test_facade: TestFacade,
):
    test_facade.given_system(address=1, name="Buy System 1", position=Point3D(0, 0, 0))
    test_facade.given_market(
        market_id=1, system_address=1, name="Buy Market 1", last_updated=None
    )
    test_facade.given_system(
        address=2, name="Sell System 2", position=Point3D(0, 10, 0)
    )
    test_facade.given_market(
        market_id=2, system_address=2, name="Sell Market 2", last_updated=None
    )
    test_facade.given_commodity(
        market_id=1, name="gold", buy=1000, sell=0, supply=1000, demand=0
    )
    test_facade.given_commodity(
        market_id=2, name="gold", buy=0, sell=2000, supply=0, demand=1000
    )

    result = handler.handle(ListTrades(buy_market=1, sell_system=2))

    assert_that(
        result,
        equal_to(
            ListTradesResult(
                trades=[
                    Trade(
                        buy_market_id=1,
                        buy_market_name="Buy Market 1",
                        sell_market_id=2,
                        sell_market_name="Sell Market 2",
                        commodity="gold",
                        buy=1000,
                        sell=2000,
                        supply=1000,
                        demand=1000,
                        profit=1000,
                        distance=0.0,
                    )
                ]
            )
        ),
    )
