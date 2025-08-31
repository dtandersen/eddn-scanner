from hamcrest import assert_that, equal_to

from scanner.command.command_factory import CommandFactory
from scanner.command.get_system import GetSystemRequest
from scanner.entity.system import Point3D, System
from scanner.repo.power_repository import PsycopgPowerRepository
from tests.facade import TestFacade


# @pytest.fixture
# def command(
#     system_repository: SystemRepository, power_repository: PsycopgPowerRepository
# ):
#     return UpdateSystem(system_repository, power_repository)


def test_system_is_added(
    command_factory: CommandFactory,
    power_repository: PsycopgPowerRepository,
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
            System(
                address=1,
                name="System 1",
                position=Point3D(x=1, y=2, z=3),
            )
        ),
    )
