--
-- depends:

CREATE TABLE public.sys_power
(
    system_address numeric NOT NULL,
    power character varying NOT NULL,
    progress numeric NOT NULL,

    PRIMARY KEY (system_address, power)
);
