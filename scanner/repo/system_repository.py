from abc import ABCMeta, abstractmethod
from typing import List

from psycopg import Connection

from scanner.entity.system import Point3D, System


class SystemRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, system: System):
        pass

    @abstractmethod
    def all(self) -> List[System]:
        pass


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
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM system")
            rows = cursor.fetchall()
            return [
                System(
                    address=row[0],
                    name=row[1],
                    position=Point3D(x=row[2], y=row[3], z=row[4]),
                )
                for row in rows
            ]
