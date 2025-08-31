import logging
from scanner.command.command_factory import CommandFactory
from scanner.command.update_system import UpdateSystemRequest
from scanner.entity.power import Power
from scanner.entity.system import Point3D
from scanner.event.discovery import DiscoveryEvent
from scanner.event.event_handler import EventBus
from scanner.event.fsd_jump import FSDJumpEvent


class SystemController:
    log = logging.getLogger(__name__)

    def __init__(
        self,
        event_bus: EventBus,
        command_factory: CommandFactory,
    ):
        self._command_factory = command_factory

        event_bus.fsd_jump.subscribe(self.on_fsd_jump)
        event_bus.discovery.subscribe(self.on_discovery)

    def on_discovery(self, event: DiscoveryEvent):
        command = self._command_factory.update_system()
        command.execute(
            UpdateSystemRequest(
                system_address=event.message.SystemAddress,
                system_name=event.message.SystemName,
                position=Point3D(
                    event.message.StarPos[0],
                    event.message.StarPos[1],
                    event.message.StarPos[2],
                ),
                state=None,
                powers=[],
            )
        )

    def on_fsd_jump(self, event: FSDJumpEvent):
        command = self._command_factory.update_system()
        powers = [
            Power(
                system_address=event.message.SystemAddress,
                progress=progress.ConflictProgress,
                name=progress.Power,
            )
            for progress in event.message.PowerplayConflictProgress
        ]
        request = UpdateSystemRequest(
            system_address=event.message.SystemAddress,
            system_name=event.message.StarSystem,
            position=Point3D(
                x=event.message.StarPos[0],
                y=event.message.StarPos[1],
                z=event.message.StarPos[2],
            ),
            state=event.message.PowerplayState,
            powers=powers,
        )
        command.execute(request)
