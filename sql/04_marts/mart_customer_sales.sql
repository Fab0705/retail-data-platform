CREATE OR REPLACE VIEW retail.mart_customer_sales AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    c.country_code,
    d.year,
    d.month_name,
    COUNT(DISTINCT f.transaction_id) AS total_orders,
    SUM(f.quantity) AS total_items_bought,
    SUM(f.quantity * f.unit_price) AS total_revenue
FROM retail.fact_sales f
JOIN retail.dim_customer c ON f.customer_key = c.customer_key
JOIN retail.dim_date d ON f.date_key = d.date_key
GROUP BY 1, 2, 3, 4, 5, 6;