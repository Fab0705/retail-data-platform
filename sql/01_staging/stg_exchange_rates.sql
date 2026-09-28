DROP TABLE IF EXISTS staging.exchange_rates;

CREATE TABLE staging.exchange_rates (
    date VARCHAR(50),
    currency_code VARCHAR(10),
    exchange_rate VARCHAR(50),
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);