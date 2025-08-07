from abc import ABCMeta, abstractmethod
from typing import List

from psycopg import Connection

from scanner.entity.market import Market


class MarketRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, market: Market):
        pass

    @abstractmethod
    def all(self) -> List[Market]:
        pass


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
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM commodity")
            rows = cursor.fetchall()
            return [
                Market(
                    market_id=row[0],
                    system_address=row[1],
                    name=row[2],
                    last_updated=row[3],
                    # market_timestamp=row[5],
                )
                for row in rows
            ]
