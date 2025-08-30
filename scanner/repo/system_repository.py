from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

from psycopg import Connection
from psycopg.rows import class_row
from scanner.entity.system import Point3D, System
from scanner.repo.market_repository import ResourceNotFoundError


class SystemRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, system: System):
        pass

    @abstractmethod
    def all(self) -> List[System]:
        pass

    @abstractmethod
    def get_system_by_name(self, name: str) -> System:
        pass

    @abstractmethod
    def get_system_by_address(self, address: int) -> System:
        pass


@dataclass
class SystemRow:
    address: int
    name: str
    x: float
    y: float
    z: float


class PsycopgSystemRepository(SystemRepository):
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, system: System):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO system (address, name, x, y, z) VALUES (%s, %s, %s, %s, %s)",
                (
                    system.address,
                    system.name,
                    system.position.x,
                    system.position.y,
                    system.position.z,
                ),
            )
            self.connection.commit()

    def all(self) -> List[System]:
        with self.connection.cursor(row_factory=class_row(SystemRow)) as cursor:
            cursor.execute("SELECT * FROM system")
            rows = cursor.fetchall()
            return [
                System(
                    address=row.address,
                    name=row.name,
                    position=Point3D(x=row.x, y=row.y, z=row.z),
                )
                for row in rows
            ]

    def get_system_by_name(self, name: str) -> System:
        with self.connection.cursor(row_factory=class_row(SystemRow)) as cursor:
            cursor.execute("SELECT * FROM system WHERE name = %s", (name,))
            row = cursor.fetchone()
            if not row:
                raise ResourceNotFoundError(f"System '{name}' not found")
            return System(
                address=int(row.address),
                name=row.name,
                position=Point3D(x=float(row.x), y=float(row.y), z=float(row.z)),
            )

    def get_system_by_address(self, address: int) -> System:
        with self.connection.cursor(row_factory=class_row(SystemRow)) as cursor:
            cursor.execute("SELECT * FROM system WHERE address = %s", (address,))
            row = cursor.fetchone()
            if not row:
                raise ResourceNotFoundError(
                    f"System with address '{address}' not found"
                )
            return System(
                address=int(row.address),
                name=row.name,
                position=Point3D(x=float(row.x), y=float(row.y), z=float(row.z)),
            )
