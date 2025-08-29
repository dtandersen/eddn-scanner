with nearby as (
select target.name, target.address, target.x, target.y, target.z, sqrt(power(target.x - center.x, 2) + power(target.y - center.y, 2) + power(target.z - center.z, 2)) as distance
from
	system as center,
	system as target
where
	center.name = 'Minerva'
	and abs(target.x - center.x) <= 35
	and abs(target.y - center.z) <= 35
	and abs(target.z - center.z) <= 35
-- order by distance
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
    buy_system.name as buy_system,
	buy_market.name as buy_station,
	sell_system.name as sell_system,
	sell_market.name as sell_station,
	c.name,
	c.buy,
	c.sell,
	c.profit,
	c.supply,
	c.demand,
	buy_market.last_update,
	sell_market.last_update
from diffs as c
join market as buy_market on c.source_market_id = buy_market.market_id and not buy_market.name like '___-___'
join market as sell_market on c.sell_market_id = sell_market.market_id
join system as buy_system on buy_market.system_address = buy_system.address
join system as sell_system on sell_market.system_address = sell_system.address
where
	c.source_market_id in (select market_id from markets)
	and profit > 10000
	and supply > 1200
	and demand > 1200

	-- and buy_market.last_update > now() - interval '60 minutes'
	-- and sell_market.last_update > now() - interval '60 minutes'
	-- and name in ('titanium', 'steel')
order by profit desc
-- order by name, buy
