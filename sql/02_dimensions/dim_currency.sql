DROP TABLE IF EXISTS retail.dim_currency CASCADE;

CREATE TABLE retail.dim_currency (
    currency_key SERIAL PRIMARY KEY,
    currency_code VARCHAR(3) NOT NULL UNIQUE,
    currency_name VARCHAR(50)
);