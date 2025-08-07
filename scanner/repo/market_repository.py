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


@dataclass
class MarketRow:
    market_id: int
    system_address: int
    name: str
    last_updated: datetime | None


class PsycopgMarketRepository(MarketRepository):
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, market: Market):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO market (market_id, system_address, name, last_update) VALUES (%s, %s, %s, %s)",
                (
                    market.market_id,
                    market.system_address,
                    market.name,
                    market.last_updated,
                ),
            )
            self.connection.commit()

    def all(self) -> List[Market]:
        with self.connection.cursor(row_factory=class_row(MarketRow)) as cursor:
            cursor.execute("SELECT * FROM commodity")
            rows = cursor.fetchall()
            return [
                Market(
                    market_id=row.market_id,
                    system_address=row.system_address,
                    name=row.name,
                    last_updated=row.last_updated,
                )
                for row in rows
            ]
