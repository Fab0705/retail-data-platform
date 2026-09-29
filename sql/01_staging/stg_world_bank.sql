DROP TABLE IF EXISTS staging.world_bank;

CREATE TABLE staging.world_bank (
    country_code VARCHAR(3),
    indicator_code VARCHAR(50),
    year VARCHAR(4),
    value NUMERIC
);