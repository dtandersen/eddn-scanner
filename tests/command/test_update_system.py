from hamcrest import assert_that, equal_to
import pytest

from scanner.command.update_system import UpdateSystem, UpdateSystemRequest
from scanner.entity.power import Power
from scanner.entity.system import Point3D, System
from scanner.event.event_handler import MessageHandler
from scanner.controller.power_controller import SystemController
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import PsycopgSystemRepository, SystemRepository
from tests.facade import TestFacade


@pytest.fixture
def command(
    system_repository: SystemRepository, power_repository: PsycopgPowerRepository
):
    return UpdateSystem(system_repository, power_repository)


def test_system_is_added(
    command: UpdateSystem,
    system_repository: SystemRepository,
    power_repository: PsycopgPowerRepository,
):
    request = UpdateSystemRequest(
        system_address=1,
        system_name="System 1",
        position=Point3D(x=1, y=2, z=3),
        state="active",
        powers=[
            Power(system_address=1, name="Power 1", progress=0.5),
            Power(system_address=1, name="Power 2", progress=0.8),
        ],
    )
    command.execute(request)

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


def test_overwrites_previous_power_progress(
    command: UpdateSystem,
    message_handler: MessageHandler,
    system_controller: SystemController,
    power_repository: PsycopgPowerRepository,
    system_repository: PsycopgSystemRepository,
    test_facade: TestFacade,
):
    system_repository.create(
        System(
            address=1,
            name="System 1",
            position=Point3D(x=3.78125, y=-147.0625, z=-33.21875),
        )
    )
    system_repository.create(
        System(
            address=2,
            name="System 2",
            position=Point3D(x=3.78125, y=-147.0625, z=-33.21875),
        )
    )
    power_repository.create(Power(system_address=1, name="Power 1", progress=0.2))
    power_repository.create(Power(system_address=1, name="Power 2", progress=0.3))
    power_repository.create(Power(system_address=1, name="Power 3", progress=0.5))
    power_repository.create(Power(system_address=2, name="Power 1", progress=0.5))
    power_repository.create(Power(system_address=2, name="Power 2", progress=0.5))

    command.execute(
        UpdateSystemRequest(
            system_address=1,
            system_name="System 1",
            position=Point3D(x=1, y=2, z=3),
            state="active",
            powers=[
                Power(system_address=1, name="Power 1", progress=0.4),
                Power(system_address=1, name="Power 2", progress=0.6),
            ],
        )
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
        powers=[],
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
