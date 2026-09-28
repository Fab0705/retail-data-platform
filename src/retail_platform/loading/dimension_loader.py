class DimensionLoader:
    def __init__(self, connection_manager):
        self.conn = connection_manager.connect()

    def upsert_customers(self):
        cursor = self.conn.cursor()
        query = """
        INSERT INTO retail.dim_customer (customer_id, customer_name, gender, country_code, customer_segment)
        SELECT customer_id, customer_name, gender, country_code, customer_segment FROM staging.customers
        ON CONFLICT (customer_id) DO UPDATE SET
            customer_name = EXCLUDED.customer_name,
            customer_segment = EXCLUDED.customer_segment;
        """
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
        print("  ✓ Dimension Customers actualizada (Upsert).")

    def upsert_products(self):
        cursor = self.conn.cursor()
        query = """
        -- Simulamos la carga desde el DataFrame procesado de productos
        """
        # Nota: Aquí implementarás consultas similares para Products y Stores
        # siguiendo la misma estructura que upsert_customers()
        pass