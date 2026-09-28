DROP TABLE IF EXISTS staging.sales;

CREATE TABLE staging.sales (
    transaction_id VARCHAR(50),
    transaction_date VARCHAR(50), -- It is read as initial text to be parsed later.
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    store_id VARCHAR(50),
    quantity VARCHAR(20),
    unit_price VARCHAR(20),
    currency_code VARCHAR(10),
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Useful load metadata
);