import logging
from scanner.command.update_powers import UpdatePowers, UpdatePowersRequest
from scanner.entity.power import Power
from scanner.entity.system import Point3D, System
from scanner.event.event_handler import EventBus
from scanner.event.fsd_jump import FSDJumpEvent
from scanner.repo.market_repository import ResourceNotFoundError
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import SystemRepository


class PowerController:
    log = logging.getLogger(__name__)

    def __init__(
        self,
        event_bus: EventBus,
        system_repository: SystemRepository,
        power_repository: PsycopgPowerRepository,
    ):
        event_bus.fsd_jump.subscribe(self.on_fsd_jump)
        self._system_repository = system_repository
        self._power_repository = power_repository

    def on_fsd_jump(self, event: FSDJumpEvent):
        try:
            _system = self._system_repository.get_system_by_address(
                event.message.SystemAddress
            )
        except ResourceNotFoundError:
            self.log.warning(f"FSDJump: Discovered system {event.message.StarSystem}")
            self._system_repository.create(
                System(
                    address=event.message.SystemAddress,
                    name=event.message.StarSystem,
                    position=Point3D(
                        x=event.message.StarPos[0],
                        y=event.message.StarPos[1],
                        z=event.message.StarPos[2],
                    ),
                )
            )
        # except psycopg.errors.UniqueViolation:
        #     pass

        if event.message.PowerplayState is None:
            return

        self.log.info(f"FSDJump: Updating powers for system {event.message.StarSystem}")

        command = UpdatePowers(self._system_repository, self._power_repository)
        powers = [
            Power(
                system_address=event.message.SystemAddress,
                progress=progress.ConflictProgress,
                name=progress.Power,
            )
            for progress in event.message.PowerplayConflictProgress
        ]
        request = UpdatePowersRequest(
            system_address=event.message.SystemAddress,
            state=event.message.PowerplayState,
            powers=powers,
        )
        command.execute(request)
