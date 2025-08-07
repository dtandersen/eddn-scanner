--
-- depends:

CREATE TABLE public.system
(
    address numeric NOT NULL PRIMARY KEY,
    "name" character varying,
    x numeric NOT NULL,
    y numeric NOT NULL,
    z numeric NOT NULL
);
