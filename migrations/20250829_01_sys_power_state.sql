--
-- depends:

CREATE TABLE public.sys_power_state
(
    system_address numeric NOT NULL PRIMARY KEY,
    power character varying NOT NULL,
    state character varying NOT NULL,
    timestamp timestamp NOT NULL
);
