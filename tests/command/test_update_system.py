import datetime
from hamcrest import assert_that, equal_to
import pytest

from scanner.command.command_factory import CommandFactory
from scanner.command.update_system import UpdateSystem, UpdateSystemRequest
from scanner.entity.power import Power
from scanner.entity.system import Point3D, System
from scanner.entity.system_state import SystemState
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import SystemRepository
from scanner.repo.system_state_repository import SystemStateRepository
from tests.facade import TestFacade


@pytest.fixture
def command(
    command_factory: CommandFactory,
):
    return command_factory.update_system()


def test_system_is_added(
    command: UpdateSystem,
    system_repository: SystemRepository,
    system_state_repository: SystemStateRepository,
    power_repository: PsycopgPowerRepository,
):
    request = UpdateSystemRequest(
        system_address=1,
        system_name="System 1",
        position=Point3D(x=1, y=2, z=3),
        state="Stronghold",
        power="Yuri Grom",
        powers=[
            Power(system_address=1, name="Power 1", progress=0.5),
            Power(system_address=1, name="Power 2", progress=0.8),
        ],
        timestamp=datetime.datetime.fromtimestamp(1234567890, datetime.timezone.utc),
    )
    command.execute(request)

    system = system_repository.get_system_by_address(1)
    assert_that(
        system,
        equal_to(
            System(
                address=1,
                name="System 1",
                position=Point3D(x=1, y=2, z=3),
            )
        ),
    )

    system_state = system_state_repository.get_system_state(1)
    assert_that(
        system_state,
        equal_to(
            SystemState(
                system_id=1,
                state="Stronghold",
                power="Yuri Grom",
                timestamp=datetime.datetime.fromtimestamp(
                    1234567890, datetime.timezone.utc
                ),
            ),
        ),
    )

    powers = power_repository.get_system_by_address(1)

    assert_that(
        powers,
        equal_to(
            [
                Power(system_address=1, name="Power 1", progress=0.5),
                Power(system_address=1, name="Power 2", progress=0.8),
            ]
        ),
    )


def test_system_state_is_updated(
    command: UpdateSystem,
    power_repository: PsycopgPowerRepository,
    system_state_repository: SystemStateRepository,
    test_facade: TestFacade,
):
    test_facade.given_system_state(
        1, "Unoccupied", None, datetime.datetime.fromtimestamp(1234567890)
    )
    test_facade.given_system(
        address=1,
        name="System 1",
        position=Point3D(x=3.78125, y=-147.0625, z=-33.21875),
    )
    test_facade.given_system(
        address=2,
        name="System 2",
        position=Point3D(x=3.78125, y=-147.0625, z=-33.21875),
    )

    test_facade.given_system_power(system_address=1, name="Power 1", progress=0.2)
    test_facade.given_system_power(system_address=1, name="Power 2", progress=0.3)
    test_facade.given_system_power(system_address=1, name="Power 3", progress=0.5)
    test_facade.given_system_power(system_address=2, name="Power 1", progress=0.5)
    test_facade.given_system_power(system_address=2, name="Power 2", progress=0.5)

    command.execute(
        UpdateSystemRequest(
            system_address=1,
            system_name="System 1",
            position=Point3D(x=1, y=2, z=3),
            state="Stronghold",
            power="Yuri Grom",
            powers=[
                Power(system_address=1, name="Power 1", progress=0.4),
                Power(system_address=1, name="Power 2", progress=0.6),
            ],
            timestamp=datetime.datetime.fromtimestamp(
                2234567890, datetime.timezone.utc
            ),
        )
    )

    system_state = system_state_repository.get_system_state(1)
    assert_that(
        system_state,
        equal_to(
            SystemState(
                system_id=1,
                state="Stronghold",
                power="Yuri Grom",
                timestamp=datetime.datetime.fromtimestamp(
                    2234567890, datetime.timezone.utc
                ),
            )
        ),
    )

    assert_that(
        power_repository.get_system_by_address(1),
        equal_to(
            [
                Power(system_address=1, name="Power 1", progress=0.4),
                Power(system_address=1, name="Power 2", progress=0.6),
            ]
        ),
        "Make sure progress for system 1 is updated",
    )

    assert_that(
        power_repository.get_system_by_address(2),
        equal_to(
            [
                Power(system_address=2, name="Power 1", progress=0.5),
                Power(system_address=2, name="Power 2", progress=0.5),
            ]
        ),
        "Make sure progress for system 2 is unchanged",
    )


def test_system_is_added2(
    command: UpdateSystem,
    system_repository: SystemRepository,
):
    request = UpdateSystemRequest(
        system_address=1,
        system_name="New System",
        position=Point3D(1, 1, 1),
        state=None,
        power=None,
        powers=[],
        timestamp=datetime.datetime.fromtimestamp(1234567890),
    )
    command.execute(request)

    system = system_repository.get_system_by_name("New System")

    assert_that(
        system,
        equal_to(
            System(
                address=1,
                name="New System",
                position=Point3D(1, 1, 1),
            )
        ),
    )


def test_existing_system_is_ignored(
    command: UpdateSystem,
    system_repository: SystemRepository,
    test_facade: TestFacade,
):
    test_facade.given_system(
        address=1, name="Existing System", position=Point3D(0, 0, 0)
    )
    request = UpdateSystemRequest(
        system_address=1,
        system_name="Existing System",
        position=Point3D(1, 1, 1),
        state=None,
        powers=[],
        power=None,
        timestamp=datetime.datetime.fromtimestamp(1234567890),
    )
    command.execute(request)

    system = system_repository.get_system_by_name("Existing System")

    assert_that(
        system,
        equal_to(
            System(
                address=1,
                name="Existing System",
                position=Point3D(0, 0, 0),
            )
        ),
    )
