DROP TABLE IF EXISTS staging.customers;

CREATE TABLE staging.customers (
    customer_id VARCHAR(50),
    customer_name VARCHAR(150),
    gender VARCHAR(50),
    country_code VARCHAR(10),
    customer_segment VARCHAR(50),
    registration_date VARCHAR(50),
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);