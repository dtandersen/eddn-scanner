--
-- depends:

CREATE TABLE public.commodity
(
    market_id numeric NOT NULL,
    "name" character varying NOT NULL,
    buy numeric,
    sell numeric,
    demand numeric,
    supply numeric,
    PRIMARY KEY (market_id, "name"),
    foreign key (market_id) references public.market(market_id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX idx_commodity_market_id_name
ON public.commodity (market_id, lower("name"));
