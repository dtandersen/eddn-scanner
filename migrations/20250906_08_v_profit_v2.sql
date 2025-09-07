--
-- depends:

CREATE OR REPLACE VIEW v_profit AS
select
	c1.market_id as buy_market_id,
	c2.market_id as sell_market_id,
	c1.name as commodity,
	c2.sell - c1.buy as profit,
	c1.buy,
	c2.sell,
	c1.supply,
	c2.demand
from
	commodity c1,
	commodity c2
where
    c1.market_id <> c2.market_id
	and lower(c1.name) = lower(c2.name)
