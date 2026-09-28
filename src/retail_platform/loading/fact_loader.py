class FactLoader:
    def __init__(self, connection_manager):
        self.conn = connection_manager.connect()

    def upsert_sales(self):
        cursor = self.conn.cursor()
        query = """
        INSERT INTO retail.fact_sales (
            transaction_id, date_key, customer_key, product_key, 
            store_key, currency_key, quantity, unit_price
        )
        SELECT 
            s.transaction_id,
            -- Generamos el date_key YYYYMMDD al vuelo o cruzamos con dim_date
            CAST(TO_CHAR(CAST(SUBSTRING(s.transaction_date, 1, 10) AS DATE), 'YYYYMMDD') AS INT),
            c.customer_key,
            p.product_key,
            st.store_key,
            curr.currency_key,
            CAST(s.quantity AS INT),
            CAST(s.unit_price AS NUMERIC)
        FROM staging.sales s
        JOIN retail.dim_customer c ON s.customer_id = c.customer_id
        JOIN retail.dim_product p ON s.product_id = p.product_id
        JOIN retail.dim_store st ON s.store_id = st.store_id
        JOIN retail.dim_currency curr ON s.currency_code = curr.currency_code
        
        -- FASE 15: Upsert en tabla de hechos
        ON CONFLICT (transaction_id, product_key) DO UPDATE SET
            quantity = EXCLUDED.quantity,
            unit_price = EXCLUDED.unit_price;
        """
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
        print("  ✓ Fact Sales actualizada (Upsert con resolución de Surrogate Keys).")