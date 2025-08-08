--
-- depends:


CREATE VIEW v_sys_dist AS
select
	s1.address as address1,
	s2.address as address2,
	sqrt(power(s1.x - s2.x, 2) + power(s1.y - s2.y, 2) + power(s1.z - s2.z, 2)) as distance
from
	system as s1,
	system as s2
