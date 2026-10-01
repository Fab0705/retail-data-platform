CREATE OR REPLACE VIEW retail.mart_product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    s.store_name,
    s.country_code AS store_country,
    d.year,
    d.month_name,
    SUM(f.quantity) AS units_sold,
    SUM(f.quantity * f.unit_price) AS total_revenue,
    AVG(f.unit_price) AS avg_selling_price
FROM retail.fact_sales f
JOIN retail.dim_product p ON f.product_key = p.product_key
JOIN retail.dim_store s ON f.store_key = s.store_key
JOIN retail.dim_date d ON f.date_key = d.date_key
GROUP BY 1, 2, 3, 4, 5, 6, 7;