from dataclasses import dataclass
from typing import Any, List, LiteralString, Sequence

from psycopg import Connection
from psycopg.rows import class_row
from scanner.entity.power import Power


@dataclass
class PowerRow:
    system_address: int
    power: str
    progress: float


class PsycopgPowerRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, power: Power):
        with self.cursor() as cursor:
            cursor.execute(
                "INSERT INTO sys_power (system_address, power, progress) VALUES (%s, %s, %s)",
                (
                    power.system_address,
                    power.name,
                    power.progress,
                ),
            )
            self.connection.commit()

    def get_system_by_address(self, system_address: int) -> List[Power]:
        return self.query(
            "SELECT * FROM sys_power WHERE system_address = %s", (system_address,)
        )

    def all(self) -> List[Power]:
        return self.query("SELECT * FROM sys_power", ())

    def delete_progress(self, system_address: int):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sys_power WHERE system_address = %s", (system_address,)
            )
            self.connection.commit()

    def query(self, sql: LiteralString, params: Sequence[Any]) -> List[Power]:
        with self.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [self.to_power(row) for row in rows]

    @staticmethod
    def to_power(row: PowerRow) -> Power:
        return Power(
            system_address=int(row.system_address),
            name=row.power,
            progress=float(row.progress),
        )

    def cursor(self):
        return self.connection.cursor(row_factory=class_row(PowerRow))
