from dataclasses import dataclass
import logging

from scanner.entity.system import Point3D, System
from scanner.repo.market_repository import ResourceNotFoundError
from scanner.repo.system_repository import SystemRepository


@dataclass
class UpdateSystemRequest:
    address: int
    name: str
    position: Point3D


class UpdateSystem:
    log = logging.getLogger(__name__)

    def __init__(
        self,
        system_repository: SystemRepository,
    ):
        self.system_repository = system_repository

    def execute(self, request: UpdateSystemRequest):
        try:
            self.system_repository.get_system_by_name(request.name)
        except ResourceNotFoundError:
            self.log.info(f"Discovered new system: {request.name}")
            self.system_repository.create(
                System(
                    address=request.address,
                    name=request.name,
                    position=request.position,
                )
            )
