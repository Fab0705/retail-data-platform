DROP TABLE IF EXISTS retail.fact_sales CASCADE;

CREATE TABLE retail.fact_sales (
    sales_key SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    date_key INT NOT NULL REFERENCES retail.dim_date(date_key),
    customer_key INT NOT NULL REFERENCES retail.dim_customer(customer_key),
    product_key INT NOT NULL REFERENCES retail.dim_product(product_key),
    store_key INT NOT NULL REFERENCES retail.dim_store(store_key),
    currency_key INT NOT NULL REFERENCES retail.dim_currency(currency_key),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    -- ETL audit metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);