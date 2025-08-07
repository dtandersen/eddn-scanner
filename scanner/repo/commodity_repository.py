from abc import ABCMeta, abstractmethod
from typing import Final, List

from psycopg import Connection

from scanner.entity.commodity import Commodity


class CommodityRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, commodity: Commodity):
        pass

    @abstractmethod
    def all(self) -> List[Commodity]:
        pass


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
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM commodity")
            rows = cursor.fetchall()
            return [
                Commodity(
                    market_id=row[0],
                    name=row[1],
                    buy=row[2],
                    sell=row[3],
                    demand=row[4],
                    supply=row[5],
                )
                for row in rows
            ]


class InMemoryCommodityRepository(CommodityRepository):
    def __init__(self):
        self.commodities: Final[List[Commodity]] = []

    def create(self, commodity: Commodity):
        self.commodities.append(commodity)

    def all(self):
        return self.commodities
