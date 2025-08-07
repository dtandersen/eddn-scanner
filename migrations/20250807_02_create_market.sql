--
-- depends:

CREATE TABLE public.market
(
    market_id numeric NOT NULL PRIMARY KEY,
    system_address numeric NOT NULL,
    "name" character varying NOT NULL,
    last_update timestamp with time zone,
    foreign key (system_address) references public.system(address) ON DELETE CASCADE
);
