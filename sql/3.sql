with nearby as (
select address2 as address
from v_sys_dist sd
where
	address1 in (select address from system where name = 'Minerva')
	and distance <= 500
),
markets as (
select *
from market as m
where m.system_address in (select address from nearby)
),
diffs as (
select
	c1.market_id as source_market_id, c2.market_id as sell_market_id, c1.name,  c2.sell - c1.buy as profit, c1.buy, c2.sell, c1.supply, c2.demand
from
	commodity c1,
	commodity c2
where
    c1.market_id <> c2.market_id
	and c1.name = c2.name
)
select
	c.name,
	c.profit,
    buy_system.name as buy_system,
	buy_market.name as buy_station,
	buy_market.station_type as buy_type,
	sell_system.name as sell_system,
	sell_market.name as sell_station,
	sell_market.station_type as sell_type,
	sd.distance,
	c.buy,
	c.sell,
	c.supply,
	c.demand,
	buy_market.last_update,
	sell_market.last_update
from diffs as c
join market as buy_market on c.source_market_id = buy_market.market_id and not buy_market.name like '___-___'
join market as sell_market on c.sell_market_id = sell_market.market_id
join system as buy_system on buy_market.system_address = buy_system.address
join system as sell_system on sell_market.system_address = sell_system.address
join v_sys_dist as sd on sd.address1 = buy_market.system_address and sd.address2 = sell_market.system_address
where
	c.source_market_id in (select market_id from markets)
	and profit > 10000
	and supply > 1200
	and demand > 1200
	and sd.distance <= 100

	and buy_market.last_update > now() - interval '1 day'
	and sell_market.last_update > now() - interval '1 day'
-- and name in ('titanium', 'steel')
order by profit desc, sd.distance asc
-- order by name, buy

-- SHOW data_directory;
