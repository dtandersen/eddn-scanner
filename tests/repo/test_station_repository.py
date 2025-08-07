from hamcrest import assert_that, equal_to
from scanner.entity.system import Point3D, System

from scanner.repo.system_repository import PsycopgSystemRepository  # type: ignore


# @pytest.fixture
# def system_repository(connection: Connection):
#     return PsycopgSystemRepository(connection)


# @pytest.mark.slow
def test_creates_commodity_in_repository(
    system_repository: PsycopgSystemRepository,
):
    system = System(
        address=1,
        name="Test System",
        position=Point3D(x=1.0, y=2.0, z=3.0),
    )
    system_repository.create(system)

    assert_that(
        system_repository.all(),
        equal_to([system]),
    )
