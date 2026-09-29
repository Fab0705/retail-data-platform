DROP TABLE IF EXISTS retail.fact_economy CASCADE;

CREATE TABLE retail.fact_economy (
    country_code VARCHAR(3),
    indicator_code VARCHAR(50),
    year INT,
    value NUMERIC,
    -- Esta es la llave que permite hacer el ON CONFLICT (Upsert)
    CONSTRAINT uk_fact_economy UNIQUE (country_code, indicator_code, year)
);