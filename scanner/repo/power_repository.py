from dataclasses import dataclass
from typing import List

from psycopg import Connection
from psycopg.rows import class_row
from scanner.entity.power import Power


@dataclass
class PowerRow:
    system_address: int
    name: str
    progress: float


class PsycopgPowerRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, power: Power):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO sys_power (system_address, name, progress) VALUES (%s, %s, %s)",
                (
                    power.system_address,
                    power.name,
                    power.progress,
                ),
            )
            self.connection.commit()

    def get_system_by_address(self, system_address: int) -> List[Power]:
        with self.connection.cursor(row_factory=class_row(PowerRow)) as cursor:
            cursor.execute(
                "SELECT * FROM sys_power WHERE system_address = %s", (system_address,)
            )
            rows = cursor.fetchall()
            return [
                Power(
                    system_address=row.system_address,
                    name=row.name,
                    progress=float(row.progress),
                )
                for row in rows
            ]
