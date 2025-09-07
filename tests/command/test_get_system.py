from datetime import datetime, timezone
from hamcrest import assert_that, equal_to
import pytest

from scanner.command.command_factory import CommandFactory
from scanner.command.get_system import GetSystem, GetSystemRequest
from scanner.dto.system import SystemDto, SystemStateDto
from scanner.entity.system import Point3D
from tests.facade import TestFacade


@pytest.fixture
def command(command_factory: CommandFactory):
    return command_factory.get_system()


def test_returns_system_and_state(
    command: GetSystem,
    test_facade: TestFacade,
):
    timestamp = datetime.now(tz=timezone.utc)
    test_facade.given_system(1, "System 1", Point3D(1, 2, 3))
    test_facade.given_system_state(1, "Stronghold", "Yuri Grom", timestamp)

    request = GetSystemRequest(
        system_address=1,
    )
    system = command.execute(request)

    assert_that(
        system,
        equal_to(
            SystemDto(
                address=1,
                name="System 1",
                position=Point3D(x=1, y=2, z=3),
                state=SystemStateDto(
                    power_state="Stronghold",
                    power="Yuri Grom",
                    timestamp=timestamp.timestamp(),
                ),
            )
        ),
    )


def test_returns_system(
    command_factory: CommandFactory,
    test_facade: TestFacade,
):
    test_facade.given_system(1, "System 1", Point3D(1, 2, 3))

    request = GetSystemRequest(
        system_address=1,
    )
    command = command_factory.get_system()
    system = command.execute(request)

    assert_that(
        system,
        equal_to(
            SystemDto(
                address=1, name="System 1", position=Point3D(x=1, y=2, z=3), state=None
            )
        ),
    )
