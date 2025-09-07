--
-- depends:

CREATE OR REPLACE FUNCTION nearby_systems(address1 numeric, distance numeric) RETURNS SETOF system AS $$
DECLARE
    center RECORD;
BEGIN
    SELECT x, y, z INTO center FROM system WHERE address = address1;
    RETURN QUERY
	    SELECT system.*
		FROM system
		-- join system as center on center.address = address1
		WHERE
		    system.x <= center.x + distance
			and system.x >= center.x - distance
			and system.y <= center.y + distance
			and system.y >= center.y - distance
			and system.z <= center.z + distance
			and system.z >= center.z - distance
			;
END;
$$ LANGUAGE plpgsql STABLE;

