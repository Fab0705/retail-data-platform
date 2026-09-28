DROP TABLE IF EXISTS retail.dim_customer CASCADE;

CREATE TABLE retail.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    country_code VARCHAR(3) NOT NULL,
    customer_segment VARCHAR(50) NOT NULL
);