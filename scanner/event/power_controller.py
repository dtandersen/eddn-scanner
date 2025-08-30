from scanner.command.update_powers import UpdatePowers, UpdatePowersRequest
from scanner.entity.power import Power
from scanner.event.event_handler import EventBus
from scanner.event.fsd_jump import FSDJumpEvent
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import SystemRepository


class PowerController:
    def __init__(
        self,
        event_bus: EventBus,
        system_repository: SystemRepository,
        power_repository: PsycopgPowerRepository,
    ):
        event_bus.fsd_jump.add_delegate(self.on_fsd_jump)
        self._system_repository = system_repository
        self._power_repository = power_repository

    def on_fsd_jump(self, event: FSDJumpEvent):
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
