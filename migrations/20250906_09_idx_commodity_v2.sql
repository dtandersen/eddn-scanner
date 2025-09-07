--
-- depends:

DROP INDEX IF EXISTS idx_commodity_supply;
DROP INDEX IF EXISTS idx_commodity_demand;

CREATE INDEX idx_commodity_supply ON commodity (market_id, lower(name), supply);
CREATE INDEX idx_commodity_demand ON commodity (market_id, lower(name), demand);
