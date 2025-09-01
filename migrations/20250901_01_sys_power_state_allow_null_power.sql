--
-- depends:

ALTER TABLE public.sys_power_state
    ALTER COLUMN power DROP NOT NULL;

ALTER TABLE public.sys_power_state
    ALTER COLUMN timestamp set data type TIMESTAMPTZ;
