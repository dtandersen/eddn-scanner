from hamcrest import assert_that, equal_to
from scanner.entity.power import Power
from scanner.entity.system import Point3D, System
from scanner.event.event_handler import MessageHandler
from scanner.controller.power_controller import SystemController
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import PsycopgSystemRepository


def test_fsd_jump_updates_power_progress(
    message_handler: MessageHandler,
    system_controller: SystemController,
    power_repository: PsycopgPowerRepository,
    system_repository: PsycopgSystemRepository,
):
    system_repository.create(
        System(
            address=670686061969,
            name="LFT 380",
            position=Point3D(
                x=-24.34375,
                y=6.1875,
                z=-57.75,
            ),
        )
    )
    message_handler.process_message(
        """
        {
            "$schemaRef": "https://eddn.edcd.io/schemas/journal/1",
            "header": {
                "gamebuild": "r317914/r0 ",
                "gameversion": "4.2.0.1",
                "gatewayTimestamp": "2025-08-28T17:04:22.116570Z",
                "softwareName": "EDDLite",
                "softwareVersion": "3.3.0.0",
                "uploaderID": "4bc909a25daa86aea08ec3b286e9aab6c75098c4"
            },
            "message": {
                "Body": "LFT 380 A",
                "BodyID": 1,
                "BodyType": "Star",
                "Factions": [
                    {
                        "Allegiance": "Federation",
                        "FactionState": "None",
                        "Government": "Democracy",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.201201,
                        "Name": "Gertrud Free"
                    },
                    {
                        "Allegiance": "Independent",
                        "FactionState": "None",
                        "Government": "Democracy",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.141141,
                        "Name": "LHS 197 Free"
                    },
                    {
                        "ActiveStates": [
                            {
                                "State": "Expansion"
                            }
                        ],
                        "Allegiance": "Federation",
                        "FactionState": "Expansion",
                        "Government": "Democracy",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.657658,
                        "Name": "The Fatherhood"
                    }
                ],
                "Population": 211939,
                "PowerplayConflictProgress": [
                    {
                        "ConflictProgress": 0.027375,
                        "Power": "Li Yong-Rui"
                    },
                    {
                        "ConflictProgress": 0.136475,
                        "Power": "Jerome Archer"
                    }
                ],
                "PowerplayState": "Unoccupied",
                "Powers": [
                    "Li Yong-Rui",
                    "Jerome Archer"
                ],
                "StarPos": [
                    -24.34375,
                    6.1875,
                    -57.75
                ],
                "StarSystem": "LFT 380",
                "SystemAddress": 670686061969,
                "SystemAllegiance": "Federation",
                "SystemEconomy": "$economy_Military;",
                "SystemFaction": {
                    "FactionState": "Expansion",
                    "Name": "The Fatherhood"
                },
                "SystemGovernment": "$government_Democracy;",
                "SystemSecondEconomy": "$economy_HighTech;",
                "SystemSecurity": "$SYSTEM_SECURITY_low;",
                "event": "FSDJump",
                "horizons": true,
                "odyssey": true,
                "timestamp": "2025-08-28T17:04:17Z"
            }
        }
        """
    )

    assert_that(
        power_repository.get_system_by_address(670686061969),
        equal_to(
            [
                Power(
                    system_address=670686061969, name="Li Yong-Rui", progress=0.027375
                ),
                Power(
                    system_address=670686061969, name="Jerome Archer", progress=0.136475
                ),
            ]
        ),
    )


# def test_adds_missing_system(
#     message_handler: MessageHandler,
#     system_controller: SystemController,
#     power_repository: PsycopgPowerRepository,
#     system_repository: PsycopgSystemRepository,
# ):
#     message_handler.process_message(
#         """
#         {
#             "$schemaRef": "https://eddn.edcd.io/schemas/journal/1",
#             "header": {
#                 "gamebuild": "r317914/r0 ",
#                 "gameversion": "4.2.0.1",
#                 "gatewayTimestamp": "2025-08-30T03:54:09.630136Z",
#                 "softwareName": "E:D Market Connector [Linux]",
#                 "softwareVersion": "5.13.1",
#                 "uploaderID": "b1a38dbf04540d199be21f5a6ae0296fb7fd9c72"
#             },
#             "message": {
#                 "Body": "Col 285 Sector EL-X d1-32",
#                 "BodyID": 0,
#                 "BodyType": "Star",
#                 "Factions": [
#                     {
#                         "Allegiance": "Independent",
#                         "FactionState": "None",
#                         "Government": "Anarchy",
#                         "Happiness": "$Faction_HappinessBand2;",
#                         "Influence": 0.02997,
#                         "Name": "Capa Gold Cartel"
#                     },
#                     {
#                         "Allegiance": "Independent",
#                         "FactionState": "None",
#                         "Government": "Feudal",
#                         "Happiness": "$Faction_HappinessBand2;",
#                         "Influence": 0.067932,
#                         "Name": "Lords of Kamil"
#                     },
#                     {
#                         "Allegiance": "Independent",
#                         "FactionState": "None",
#                         "Government": "Democracy",
#                         "Happiness": "$Faction_HappinessBand2;",
#                         "Influence": 0.096903,
#                         "Name": "HIP 36560 Democrats"
#                     },
#                     {
#                         "ActiveStates": [
#                             {
#                                 "State": "Expansion"
#                             }
#                         ],
#                         "Allegiance": "Alliance",
#                         "FactionState": "Expansion",
#                         "Government": "Democracy",
#                         "Happiness": "$Faction_HappinessBand2;",
#                         "Influence": 0.805195,
#                         "Name": "Flat Galaxy Society"
#                     }
#                 ],
#                 "Multicrew": false,
#                 "Population": 390174881,
#                 "StarPos": [
#                     116.46875,
#                     83.125,
#                     -201.34375
#                 ],
#                 "StarSystem": "Col 285 Sector EL-X d1-32",
#                 "SystemAddress": 1110022572371,
#                 "SystemAllegiance": "Alliance",
#                 "SystemEconomy": "$economy_Agri;",
#                 "SystemFaction": {
#                     "FactionState": "Expansion",
#                     "Name": "Flat Galaxy Society"
#                 },
#                 "SystemGovernment": "$government_Democracy;",
#                 "SystemSecondEconomy": "$economy_Tourism;",
#                 "SystemSecurity": "$SYSTEM_SECURITY_medium;",
#                 "Taxi": false,
#                 "event": "FSDJump",
#                 "horizons": true,
#                 "odyssey": true,
#                 "timestamp": "2025-08-30T03:54:08Z"
#             }
#         }
#         """
#     )

#     assert_that(
#         system_repository.get_system_by_address(1110022572371),
#         equal_to(
#             System(
#                 address=1110022572371,
#                 name="Col 285 Sector EL-X d1-32",
#                 position=Point3D(116.46875, 83.125, -201.34375),
#             )
#         ),
#     )

#     assert_that(
#         power_repository.all(),
#         equal_to([]),
#     )


def test_fsd_jump_without_power_progress(
    message_handler: MessageHandler,
    system_controller: SystemController,
    power_repository: PsycopgPowerRepository,
    system_repository: PsycopgSystemRepository,
):
    system_repository.create(
        System(
            address=670686061969,
            name="LFT 380",
            position=Point3D(
                x=-24.34375,
                y=6.1875,
                z=-57.75,
            ),
        )
    )
    message_handler.process_message(
        """
        {
            "$schemaRef": "https://eddn.edcd.io/schemas/journal/1",
            "header": {
                "gamebuild": "r317914/r0 ",
                "gameversion": "4.2.0.1",
                "gatewayTimestamp": "2025-08-30T06:56:17.862467Z",
                "softwareName": "EDO Materials Helper",
                "softwareVersion": "2.243",
                "uploaderID": "2d1aee310e11f02c5accfe6da5f2e7640a610a27"
            },
            "message": {
                "Body": "LHS 1197 A",
                "BodyID": 1,
                "BodyType": "Star",
                "Conflicts": [
                    {
                        "Faction1": {
                            "Name": "League of LHS 1197 Party",
                            "Stake": "Burn Obligation",
                            "WonDays": 0
                        },
                        "Faction2": {
                            "Name": "Black Lotus",
                            "Stake": "",
                            "WonDays": 0
                        },
                        "Status": "pending",
                        "WarType": "civilwar"
                    }
                ],
                "ControllingPower": "Jerome Archer",
                "Factions": [
                    {
                        "Allegiance": "Federation",
                        "FactionState": "None",
                        "Government": "Corporate",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.043,
                        "Name": "LHS 1197 Inc",
                        "RecoveringStates": [
                            {
                                "State": "PublicHoliday",
                                "Trend": 0
                            }
                        ]
                    },
                    {
                        "Allegiance": "Independent",
                        "FactionState": "None",
                        "Government": "Dictatorship",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.037,
                        "Name": "LHS 1197 Flag"
                    },
                    {
                        "Allegiance": "Independent",
                        "FactionState": "None",
                        "Government": "Anarchy",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.017,
                        "Name": "LHS 1197 Gold Family"
                    },
                    {
                        "ActiveStates": [
                            {
                                "State": "Boom"
                            }
                        ],
                        "Allegiance": "Federation",
                        "FactionState": "Boom",
                        "Government": "Democracy",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.108,
                        "Name": "Independent LHS 1197 Values Party"
                    },
                    {
                        "Allegiance": "Independent",
                        "FactionState": "None",
                        "Government": "Dictatorship",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.077,
                        "Name": "League of LHS 1197 Party",
                        "PendingStates": [
                            {
                                "State": "CivilWar",
                                "Trend": 0
                            }
                        ]
                    },
                    {
                        "ActiveStates": [
                            {
                                "State": "Boom"
                            },
                            {
                                "State": "Expansion"
                            }
                        ],
                        "Allegiance": "Independent",
                        "FactionState": "Expansion",
                        "Government": "Democracy",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.641,
                        "Name": "Paladin Consortium"
                    },
                    {
                        "Allegiance": "Federation",
                        "FactionState": "None",
                        "Government": "Democracy",
                        "Happiness": "$Faction_HappinessBand2;",
                        "Influence": 0.077,
                        "Name": "Black Lotus",
                        "PendingStates": [
                            {
                                "State": "CivilWar",
                                "Trend": 0
                            }
                        ]
                    }
                ],
                "Multicrew": false,
                "Population": 13662847,
                "PowerplayState": "Stronghold",
                "PowerplayStateControlProgress": 0.316677,
                "PowerplayStateReinforcement": 10657,
                "PowerplayStateUndermining": 14780,
                "Powers": [
                    "Aisling Duval",
                    "Denton Patreus",
                    "Li Yong-Rui",
                    "Yuri Grom",
                    "Zemina Torval",
                    "Jerome Archer"
                ],
                "StarPos": [
                    2.5625,
                    -42.8125,
                    -1.625
                ],
                "StarSystem": "LHS 1197",
                "SystemAddress": 13865093899689,
                "SystemAllegiance": "Independent",
                "SystemEconomy": "$economy_HighTech;",
                "SystemFaction": {
                    "FactionState": "Expansion",
                    "Name": "Paladin Consortium"
                },
                "SystemGovernment": "$government_Democracy;",
                "SystemSecondEconomy": "$economy_Refinery;",
                "SystemSecurity": "$SYSTEM_SECURITY_high;",
                "Taxi": false,
                "event": "FSDJump",
                "horizons": true,
                "odyssey": true,
                "timestamp": "2025-08-30T06:56:11Z"
            }
        }
        """
    )

    # assert_that(
    #     power_repository.get_system_by_address(670686061969),
    #     equal_to(
    #         [
    #             Power(
    #                 system_address=670686061969, name="Li Yong-Rui", progress=0.027375
    #             ),
    #             Power(
    #                 system_address=670686061969, name="Jerome Archer", progress=0.136475
    #             ),
    #         ]
    #     ),
    # )


def test_fss_discovery_scan_updates_system(
    system_repository: PsycopgSystemRepository,
    message_handler: MessageHandler,
    system_controller: SystemController,
):
    message_handler.process_message(
        """
        {
            "$schemaRef": "https://eddn.edcd.io/schemas/fssdiscoveryscan/1",
            "header": {
                "gamebuild": "r316268/r0 ",
                "gameversion": "4.1.3.0",
                "gatewayTimestamp": "2025-08-07T18:25:09.281149Z",
                "softwareName": "EDO Materials Helper",
                "softwareVersion": "2.221",
                "uploaderID": "3b9e71f3f8e276e389065e70026fb905901f671e"
            },
            "message": {
                "BodyCount": 15,
                "NonBodyCount": 59,
                "StarPos": [
                    51.40625,
                    -54.40625,
                    -30.5
                ],
                "SystemAddress": 1458309141194,
                "SystemName": "Eurybia",
                "event": "FSSDiscoveryScan",
                "horizons": true,
                "odyssey": true,
                "timestamp": "2025-08-07T18:25:02Z"
            }
        }
        """
    )

    assert_that(
        system_repository.get_system_by_name("Eurybia"),
        equal_to(
            System(
                address=1458309141194,
                name="Eurybia",
                position=Point3D(51.40625, -54.40625, -30.5),
            ),
        ),
    )
