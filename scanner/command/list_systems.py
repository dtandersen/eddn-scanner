from dataclasses import dataclass
from scanner.repo.system_repository import SystemRepository


@dataclass
class ListSystemsRequest:
    name: str


class ListSystems:
    def __init__(self, system_repository: SystemRepository):
        self.system_repository = system_repository

    def execute(self, request: ListSystemsRequest):
        systems = self.system_repository.find_system_by_name(request.name)
        return systems
