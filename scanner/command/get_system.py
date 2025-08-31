from dataclasses import dataclass
from scanner.repo.system_repository import SystemRepository


@dataclass
class GetSystemRequest:
    system_address: int


class GetSystem:
    def __init__(self, system_repository: SystemRepository):
        self.system_repository = system_repository

    def execute(self, request: GetSystemRequest):
        return self.system_repository.get_system_by_address(request.system_address)
