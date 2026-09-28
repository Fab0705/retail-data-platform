DROP TABLE IF EXISTS retail.dim_product CASCADE;

CREATE TABLE retail.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    brand VARCHAR(50)
);