from datetime import datetime
from hamcrest import assert_that, equal_to
from scanner.entity.commodity import Commodity
from scanner.event.eddb_handler import CommodityEddnHandler, CommodityWriter
from scanner.event.event_handler import EventBus
from scanner.repo.commodity_repository import InMemoryCommodityRepository


def test_handles_commodities_event():
    commodity_repository = InMemoryCommodityRepository()
    bus = EventBus()
    _writer = CommodityWriter(bus, commodity_repository)
    events = CommodityEddnHandler(bus)
    events.handle(
        {
            "$schemaRef": "https://eddn.edcd.io/schemas/commodity/3",
            "header": {
                "gamebuild": "",
                "gameversion": "CAPI-Live-market",
                "gatewayTimestamp": "2025-08-07T04:29:41.647517Z",
                "softwareName": "E:D Market Connector [Windows]",
                "softwareVersion": "5.13.1",
                "uploaderID": "df357959129a5486b2893c71ffd5215be97b6ee4",
            },
            "message": {
                "commodities": [
                    {
                        "buyPrice": 0,
                        "demand": 117,
                        "demandBracket": 3,
                        "meanPrice": 2863,
                        "name": "advancedcatalysers",
                        "sellPrice": 3424,
                        "stock": 0,
                        "stockBracket": 0,
                    }
                ],
                "economies": [{"name": "Carrier", "proportion": 1}],
                "horizons": False,
                "marketId": 3712635648,
                "odyssey": True,
                "prohibited": [
                    "ApaVietii",
                    "BasicNarcotics",
                    "Beer",
                    "BootlegLiquor",
                    "Liquor",
                    "Tobacco",
                    "Wine",
                ],
                "stationName": "K2N-WTT",
                "systemName": "HR 1185",
                "timestamp": "2025-08-07T04:29:40Z",
            },
        }
    )

    assert_that(
        commodity_repository.all(),
        equal_to(
            [
                Commodity(
                    timestamp=datetime.fromisoformat("2025-08-07T04:29:40Z"),
                    name="advancedcatalysers",
                    buy=0,
                    sell=3424,
                    supply=0,
                    demand=117,
                    station="K2N-WTT",
                    system="HR 1185",
                ),
            ]
        ),
    )
