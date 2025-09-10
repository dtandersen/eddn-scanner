from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from psycopg import Connection
from psycopg.rows import class_row

from scanner.dto.trade import Trade
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


@dataclass
class TradeRow:
    buy_system: str
    buy_market_id: int
    buy_station: str
    sell_system: str
    sell_market_id: int
    sell_station: str
    commodity: str
    buy: int
    sell: int
    supply: int
    demand: int
    profit: int
    distance: float
    last_update: int


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

    def get_trades(
        self,
        buy_market_id: int,
        sell_market_id: Optional[int],
        sell_system_id: Optional[int],
    ) -> list[Trade]:
        sql = """
        with
        profit as (
            select
                buy.market_id as buy_market_id,
                sell.market_id as sell_market_id,
                buy.name as commodity,
                sell.sell - buy.buy as profit,
                buy.buy,
                sell.sell,
                buy.supply,
                sell.demand
            from
                commodity buy,
                commodity sell
            where
                buy.market_id = %(buy_market_id)s
                and (sell.market_id = %(sell_market_id)s or sell.market_id in (select market_id from market where system_address = %(sell_system_id)s))
                and buy.market_id <> sell.market_id
                and lower(buy.name) = lower(sell.name)
        )
        select
            buy_system.name as buy_system,
            buy_market.name as buy_station,
            c.buy_market_id,
            sell_system.name as sell_system,
            sell_market.name as sell_station,
            c.sell_market_id,
            c.commodity,
            c.buy,
            c.sell,
            c.profit,
            c.supply,
            c.demand,
            buy_market.last_update,
            sell_market.last_update,
            0 as distance
        from
        profit c
        join market as buy_market on c.buy_market_id = buy_market.market_id
        join market as sell_market on c.sell_market_id = sell_market.market_id
        join system as buy_system on buy_market.system_address = buy_system.address
        join system as sell_system on sell_market.system_address = sell_system.address
        order by profit desc
        limit 100
        """

        params = {
            "buy_market_id": buy_market_id,
            "sell_market_id": sell_market_id,
            "sell_system_id": sell_system_id,
        }
        with self.connection.cursor(row_factory=class_row(TradeRow)) as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [
                Trade(
                    buy_market_id=int(row.buy_market_id),
                    buy_market_name=row.buy_station,
                    sell_market_id=int(row.sell_market_id),
                    sell_market_name=row.sell_station,
                    commodity=row.commodity,
                    buy=int(row.buy),
                    sell=int(row.sell),
                    demand=int(row.demand),
                    supply=int(row.supply),
                    profit=int(row.profit),
                    distance=float(row.distance),
                )
                for row in rows
            ]
