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


class PsycogCommodityRepository(CommodityRepository):
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, commodity: Commodity):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO commodity (timestamp, name, buy, sell, supply, demand, station, system) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    commodity.timestamp,
                    commodity.name,
                    commodity.buy,
                    commodity.sell,
                    commodity.supply,
                    commodity.demand,
                    commodity.station,
                    commodity.system,
                ),
            )
            self.connection.commit()

    def all(self) -> List[Commodity]:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM commodity")
            rows = cursor.fetchall()
            return [
                Commodity(
                    timestamp=row[0],
                    station=row[1],
                    system=row[2],
                    name=row[3],
                    buy=row[4],
                    sell=row[5],
                    demand=row[6],
                    supply=row[7],
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
