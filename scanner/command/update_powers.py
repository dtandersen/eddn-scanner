from dataclasses import dataclass
import logging

from scanner.entity.power import Power
from scanner.repo.power_repository import PsycopgPowerRepository
from scanner.repo.system_repository import SystemRepository


@dataclass
class UpdatePowersRequest:
    system_address: int
    state: str
    powers: list[Power]


class UpdatePowers:
    log = logging.getLogger(__name__)

    def __init__(
        self,
        system_repository: SystemRepository,
        power_repository: PsycopgPowerRepository,
    ):
        self.system_repository = system_repository
        self.power_repository = power_repository

    def execute(self, request: UpdatePowersRequest):
        self.power_repository.delete_progress(request.system_address)
        for power in request.powers:
            self.power_repository.create(power)
