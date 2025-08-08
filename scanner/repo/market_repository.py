from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from psycopg import Connection
from psycopg.rows import class_row

from scanner.entity.market import Market


class MarketRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, market: Market):
        pass

    @abstractmethod
    def all(self) -> List[Market]:
        pass

    @abstractmethod
    def get_market(self, market_id: int) -> Market:
        pass

    @abstractmethod
    def update_timestamp(self, market_id: int, timestamp: datetime):
        pass


@dataclass
class MarketRow:
    market_id: int
    system_address: int
    name: str
    last_update: datetime | None
    station_type: str | None
    docking_access: str | None


class ResourceNotFoundError(Exception):
    pass


class PsycopgMarketRepository(MarketRepository):
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, market: Market):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO market (market_id, system_address, name, station_type, docking_access, last_update) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    market.market_id,
                    market.system_address,
                    market.name,
                    market.station_type,
                    market.docking_access,
                    market.last_updated,
                ),
            )
            self.connection.commit()

    def all(self) -> List[Market]:
        with self.connection.cursor(row_factory=class_row(MarketRow)) as cursor:
            cursor.execute("SELECT * FROM market")
            rows = cursor.fetchall()
            return [
                Market(
                    market_id=int(row.market_id),
                    system_address=int(row.system_address),
                    name=row.name,
                    station_type=row.station_type,
                    docking_access=row.docking_access,
                    last_updated=row.last_update,
                )
                for row in rows
            ]

    def get_market(self, market_id: int) -> Market:
        with self.connection.cursor(row_factory=class_row(MarketRow)) as cursor:
            cursor.execute("SELECT * FROM market WHERE market_id = %s", (market_id,))
            row = cursor.fetchone()
            if row is None:
                raise ResourceNotFoundError(f"Market {market_id} not found")
            return Market(
                market_id=int(row.market_id),
                system_address=int(row.system_address),
                name=row.name,
                station_type=row.station_type,
                docking_access=row.docking_access,
                last_updated=row.last_update,
            )

    def update_timestamp(self, market_id: int, timestamp: datetime):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE market SET last_update = %s WHERE market_id = %s",
                (timestamp, market_id),
            )
            self.connection.commit()
