from hamcrest import assert_that, equal_to
from scanner.entity.power import Power
from scanner.event.event_handler import MessageHandler
from scanner.event.power_controller import PowerController
from scanner.repo.power_repository import PsycopgPowerRepository


def test_handles_commodities_event(
    message_handler: MessageHandler,
    _power_controller: PowerController,
    power_repository: PsycopgPowerRepository,
):
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
