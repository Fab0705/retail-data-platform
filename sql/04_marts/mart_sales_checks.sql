CREATE OR REPLACE VIEW retail.mart_sales_checks AS
WITH yearly_sales AS (
    SELECT 
        s.country_code,
        d.year,
        SUM(f.quantity * f.unit_price) AS total_sales
    FROM retail.fact_sales f
    JOIN retail.dim_store s ON f.store_key = s.store_key
    JOIN retail.dim_date d ON f.date_key = d.date_key
    GROUP BY 1, 2
)
SELECT 
    ys.country_code,
    ys.year,
    ys.total_sales,
    e.indicator_code,
    e.value AS economic_indicator_value
FROM yearly_sales ys
LEFT JOIN retail.fact_economy e 
    ON ys.country_code = e.country_code 
    AND ys.year = e.year;