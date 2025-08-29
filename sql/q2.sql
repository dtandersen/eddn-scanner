select *
from commodity as c
join market as m on c.market_id = m.market_id
where m.name like '___-___'
and c.sell > 10000
and c.demand > 1200
and last_update > now() - interval '6 hour'
order by sell desc, m.name
