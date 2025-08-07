from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

from psycopg import Connection
from psycopg.rows import class_row

from scanner.entity.commodity import Commodity


class CommodityRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, commodity: Commodity):
        pass

    @abstractmethod
    def all(self) -> List[Commodity]:
        pass

    @abstractmethod
    def delete_market(self, market_id: int):
        pass


@dataclass
class CommodityRow:
    market_id: int
    name: str
    buy: int
    sell: int
    supply: int
    demand: int


class PsycopgCommodityRepository(CommodityRepository):
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, commodity: Commodity):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO commodity (market_id, name, buy, sell, supply, demand) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    commodity.market_id,
                    commodity.name,
                    commodity.buy,
                    commodity.sell,
                    commodity.supply,
                    commodity.demand,
                ),
            )
            self.connection.commit()

    def all(self) -> List[Commodity]:
        with self.connection.cursor(row_factory=class_row(CommodityRow)) as cursor:
            cursor.execute("SELECT * FROM commodity")
            rows = cursor.fetchall()
            return [
                Commodity(
                    market_id=row.market_id,
                    name=row.name,
                    buy=row.buy,
                    sell=row.sell,
                    demand=row.demand,
                    supply=row.supply,
                )
                for row in rows
            ]

    def delete_market(self, market_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM commodity WHERE market_id = %s", (market_id,))
            self.connection.commit()
