--
-- depends:

CREATE VIEW v_market_dist AS
SELECT
  sd.address1,
  m1.market_id as market1,
  sd.address2,
  m2.market_id as market2,
  sd.distance
FROM v_sys_dist as sd
JOIN market as m1 on m1.system_address = sd.address1
JOIN market as m2 on m2.system_address = sd.address2
