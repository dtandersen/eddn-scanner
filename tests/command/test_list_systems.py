from hamcrest import assert_that, equal_to

from scanner.command.command_factory import CommandFactory
from scanner.command.list_systems import ListSystemsRequest
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
    test_facade.given_system(2, "System 2", Point3D(1, 2, 3))

    request = ListSystemsRequest(
        name="system",
    )
    command = command_factory.list_systems()
    systems = command.execute(request)

    assert_that(
        systems,
        equal_to(
            [
                System(
                    address=1,
                    name="System 1",
                    position=Point3D(x=1, y=2, z=3),
                ),
                System(
                    address=2,
                    name="System 2",
                    position=Point3D(x=1, y=2, z=3),
                ),
            ]
        ),
    )
