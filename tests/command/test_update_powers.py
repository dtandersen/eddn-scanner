from hamcrest import assert_that, equal_to
import pytest

from scanner.command.update_powers import UpdatePowers, UpdatePowersRequest
from scanner.entity.power import Power
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import SystemRepository


@pytest.fixture
def command(
    system_repository: SystemRepository, power_repository: PsycopgPowerRepository
):
    return UpdatePowers(system_repository, power_repository)


def test_system_is_added(
    command: UpdatePowers,
    system_repository: SystemRepository,
    power_repository: PsycopgPowerRepository,
):
    request = UpdatePowersRequest(
        system_address=1,
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
