DROP TABLE IF EXISTS retail.dim_store CASCADE;

CREATE TABLE retail.dim_store (
    store_key SERIAL PRIMARY KEY,
    store_id VARCHAR(50) NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(3) NOT NULL,
    city VARCHAR(100),
    store_type VARCHAR(50)
);