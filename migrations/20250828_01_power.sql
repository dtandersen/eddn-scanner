--
-- depends:

CREATE TABLE public.sys_power
(
    system_address numeric NOT NULL,
    "name" character varying NOT NULL,
    progress numeric NOT NULL,

     PRIMARY KEY (system_address, name)
);
