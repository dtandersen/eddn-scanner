from datetime import datetime
from hamcrest import assert_that, equal_to
from scanner.entity.commodity import Commodity
from scanner.entity.market import Market
from scanner.entity.system import Point3D, System
from scanner.controller.commodity_controller import CommodityController
from scanner.event.event_handler import MessageHandler
from scanner.repo.commodity_repository import PsycopgCommodityRepository
from scanner.repo.market_repository import PsycopgMarketRepository
from scanner.repo.system_repository import PsycopgSystemRepository


def test_handles_commodities_event(
    commodity_repository: PsycopgCommodityRepository,
    system_repository: PsycopgSystemRepository,
    market_repository: PsycopgMarketRepository,
    message_handler: MessageHandler,
    commodity_controller: CommodityController,
):
    system_repository.create(
        System(address=1, name="HR 1185", position=Point3D(0, 0, 0))
    )

    message_handler.process_message(
        """
        {
            "$schemaRef": "https://eddn.edcd.io/schemas/commodity/3",
            "header": {
                "gamebuild": "",
                "gameversion": "CAPI-Live-market",
                "gatewayTimestamp": "2025-08-07T04:29:41.647517Z",
                "softwareName": "E:D Market Connector [Windows]",
                "softwareVersion": "5.13.1",
                "uploaderID": "df357959129a5486b2893c71ffd5215be97b6ee4"
            },
            "message": {
                "carrierDockingAccess": "all",
                "commodities": [
                    {
                        "buyPrice": 0,
                        "demand": 117,
                        "demandBracket": 3,
                        "meanPrice": 2863,
                        "name": "advancedcatalysers",
                        "sellPrice": 3424,
                        "stock": 0,
                        "stockBracket": 0
                    }
                ],
                "economies": [
                    {
                        "name": "Carrier",
                        "proportion": 1
                    }
                ],
                "horizons": false,
                "marketId": 3712635648,
                "odyssey": true,
                "prohibited": [
                    "ApaVietii",
                    "BasicNarcotics",
                    "Beer",
                    "BootlegLiquor",
                    "Liquor",
                    "Tobacco",
                    "Wine"
                ],
                "stationName": "K2N-WTT",
                "stationType": "FleetCarrier",
                "systemName": "HR 1185",
                "timestamp": "2025-08-07T04:29:40Z"
            }
        }
        """
    )

    assert_that(
        commodity_repository.all(),
        equal_to(
            [
                Commodity(
                    market_id=3712635648,
                    name="advancedcatalysers",
                    buy=0,
                    sell=3424,
                    supply=0,
                    demand=117,
                ),
            ]
        ),
    )

    assert_that(
        market_repository.get_market(3712635648),
        equal_to(
            Market(
                system_address=1,
                market_id=3712635648,
                name="K2N-WTT",
                last_updated=datetime.fromisoformat("2025-08-07T04:29:40Z"),
                station_type="FleetCarrier",
                docking_access="all",
            ),
        ),
    )
