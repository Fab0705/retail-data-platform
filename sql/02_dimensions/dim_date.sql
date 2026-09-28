DROP TABLE IF EXISTS retail.dim_date CASCADE;

CREATE TABLE retail.dim_date (
    date_key INT PRIMARY KEY, -- Formato YYYYMMDD
    full_date DATE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week VARCHAR(20) NOT NULL
);