from hamcrest import assert_that, equal_to
import pytest

from scanner.command.update_system import UpdateSystem, UpdateSystemRequest
from scanner.entity.system import Point3D, System
from scanner.repo.system_repository import SystemRepository
from tests.facade import TestFacade


@pytest.fixture
def command(
    system_repository: SystemRepository,
):
    return UpdateSystem(system_repository)


def test_system_is_added(
    command: UpdateSystem,
    system_repository: SystemRepository,
):
    request = UpdateSystemRequest(
        address=1,
        name="New System",
        position=Point3D(1, 1, 1),
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
        address=1,
        name="Existing System",
        position=Point3D(1, 1, 1),
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
