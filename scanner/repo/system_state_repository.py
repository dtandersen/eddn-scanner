from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from psycopg import Connection
from psycopg.rows import class_row

from scanner.entity.system_state import SystemState


@dataclass
class SystemStateRow:
    system_address: int
    state: str
    power: Optional[str]
    timestamp: datetime


class SystemStateRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    def get_system_state(self, system_id: int) -> SystemState:
        with self.connection.cursor(row_factory=class_row(SystemStateRow)) as cursor:
            cursor.execute(
                "SELECT * FROM sys_power_state WHERE system_address = %s", (system_id,)
            )
            row = cursor.fetchone()
            if row is None:
                raise ValueError(f"System state with address {system_id} not found")
            return SystemState(
                system_id=int(row.system_address),
                state=row.state,
                power=row.power,
                timestamp=row.timestamp,
            )

    def update_system_state(self, state: SystemState):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sys_power_state (system_address, state, power, timestamp)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (system_address) DO UPDATE
                SET state = EXCLUDED.state,
                    power = EXCLUDED.power,
                    timestamp = EXCLUDED.timestamp
                """,
                (state.system_id, state.state, state.power, state.timestamp),
            )
            self.connection.commit()
