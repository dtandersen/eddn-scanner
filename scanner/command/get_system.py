from dataclasses import dataclass
from scanner.dto.system import SystemDto, SystemStateDto
from scanner.repo.system_repository import SystemRepository
from scanner.repo.system_state_repository import SystemStateRepository


@dataclass
class GetSystemRequest:
    system_address: int


class GetSystem:
    def __init__(
        self,
        system_repository: SystemRepository,
        system_state_repository: SystemStateRepository,
    ):
        self.system_repository = system_repository
        self.system_state_repository = system_state_repository

    def execute(self, request: GetSystemRequest):
        system = self.system_repository.get_system_by_address(request.system_address)
        try:
            state = self.system_state_repository.get_system_state(
                request.system_address
            )
        except ValueError:
            state = None

        return SystemDto(
            address=system.address,
            name=system.name,
            position=system.position,
            state=(
                SystemStateDto(
                    power=state.power if state else None,
                    power_state=state.state if state else None,
                    timestamp=(
                        state.timestamp.timestamp()
                        if state and state.timestamp
                        else None
                    ),
                )
                if state
                else None
            ),
        )
