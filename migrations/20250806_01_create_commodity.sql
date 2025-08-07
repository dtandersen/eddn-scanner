--
-- depends:

CREATE TABLE public.commodity
(
    "timestamp" timestamp with time zone NOT NULL,
    station character varying,
    system character varying,
    "name" character varying NOT NULL,
    buy integer,
    sell integer,
    demand integer,
    supply integer
);
