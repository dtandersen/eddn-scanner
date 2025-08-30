from dataclasses import dataclass
import logging
from typing import List, Optional

from scanner.entity.power import Power
from scanner.entity.system import Point3D, System
from scanner.repo.market_repository import ResourceNotFoundError
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import SystemRepository


@dataclass
class UpdateSystemRequest:
    system_address: int
    system_name: str
    position: Point3D
    state: Optional[str]
    powers: List[Power]


class UpdateSystem:
    log = logging.getLogger(__name__)

    def __init__(
        self,
        system_repository: SystemRepository,
        power_repository: PsycopgPowerRepository,
    ):
        self.system_repository = system_repository
        self.power_repository = power_repository

    def execute(self, request: UpdateSystemRequest):
        self.log.info(f"Updating system {request.system_name}")

        try:
            self.system_repository.get_system_by_name(request.system_name)
        except ResourceNotFoundError:
            self.log.info(f"Discovered new system: {request.system_name}")
            self.system_repository.create(
                System(
                    address=request.system_address,
                    name=request.system_name,
                    position=request.position,
                )
            )

        self.power_repository.delete_progress(request.system_address)
        for power in request.powers:
            self.power_repository.create(power)
