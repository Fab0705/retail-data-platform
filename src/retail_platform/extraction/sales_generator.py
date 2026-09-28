import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import uuid

class RetailDataGenerator:
    def __init__(self, start_year=2018, end_year=2025):
        self.start_year = start_year
        self.end_year = end_year
        # We define the countries and their corresponding currencies for consistency in sales generation
        self.countries = ['PER', 'BRA', 'CHL', 'COL', 'MEX']
        self.currencies = {'PER': 'PEN', 'BRA': 'BRL', 'CHL': 'CLP', 'COL': 'COP', 'MEX': 'MXN'}
        
        # Semilla para que los datos sean reproducibles cada vez que ejecutes el script
        random.seed(42)
        np.random.seed(42)

    def _random_date(self, start_date, end_date):
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        return start_date + timedelta(days=random_number_of_days)

    def generate_stores(self):
        """Genera tiendas asegurando que haya presencia en los 5 países."""
        stores = []
        for i, country in enumerate(self.countries):
            # Creamos 2 tiendas por país para dar variedad
            for j in range(2):
                stores.append({
                    'store_id': f"ST-{country}-{j+1}",
                    'store_name': f"MegaStore {country} {j+1}",
                    'country_code': country,
                    'city': f"Capital of {country}",
                    'store_type': random.choice(['Mall', 'Street', 'Outlet'])
                })
        return pd.DataFrame(stores)

    def generate_products(self, num_products=50):
        """Genera un catálogo maestro de productos."""
        categories = ['Electronics', 'Clothing', 'Home', 'Sports']
        products = []
        
        for i in range(1, num_products + 1):
            category = random.choice(categories)
            unit_cost = round(random.uniform(10.0, 500.0), 2)
            # El precio de venta es el costo + un margen del 30% al 80%
            unit_price = round(unit_cost * random.uniform(1.3, 1.8), 2)
            
            products.append({
                'product_id': f"PRD-{str(i).zfill(4)}",
                'product_name': f"{category} Item {i}",
                'category': category,
                'brand': f"Brand{random.randint(1, 10)}",
                'unit_cost': unit_cost,
                'unit_price': unit_price
            })
        return pd.DataFrame(products)

    def generate_customers(self, num_customers=1000):
        """Genera clientes asignados aleatoriamente a un país."""
        start_date = datetime(self.start_year, 1, 1)
        end_date = datetime(self.end_year, 12, 31)
        
        customers = []
        for i in range(1, num_customers + 1):
            customers.append({
                'customer_id': f"CUST-{str(i).zfill(5)}",
                'customer_name': f"Customer {i}",
                'gender': random.choice(['M', 'F', 'Other', 'N/A']),
                'country_code': random.choice(self.countries),
                'customer_segment': random.choice(['Standard', 'Premium', 'VIP']),
                'registration_date': self._random_date(start_date, end_date).strftime('%Y-%m-%d')
            })
        return pd.DataFrame(customers)

    def generate_sales(self, customers_df, products_df, stores_df, num_orders=5000):
        """
        Genera transacciones aplicando las reglas de consistencia de la Fase 9:
        - El cliente debe comprar en una tienda de su mismo país.
        - Los IDs de productos y clientes deben existir en sus respectivos DataFrames.
        """
        start_date = datetime(self.start_year, 1, 1)
        end_date = datetime(self.end_year, 12, 31)
        
        sales_lines = []
        
        # Listas para optimizar la búsqueda aleatoria (mucho más rápido en Python)
        customer_records = customers_df.to_dict('records')
        product_records = products_df.to_dict('records')
        
        for _ in range(num_orders):
            # 1. Seleccionamos un cliente válido de la dimensión
            customer = random.choice(customer_records)
            
            # 2. CONSISTENCIA: Filtramos las tiendas para que coincidan con el país del cliente
            valid_stores = stores_df[stores_df['country_code'] == customer['country_code']]['store_id'].tolist()
            store_id = random.choice(valid_stores)
            
            # 3. Datos generales de la orden
            transaction_id = f"TRX-{uuid.uuid4().hex[:8].upper()}"
            # Aseguramos que la compra sea DESPUÉS del registro del cliente
            reg_date = datetime.strptime(customer['registration_date'], '%Y-%m-%d')
            transaction_date = self._random_date(reg_date, end_date)
            currency = self.currencies[customer['country_code']]
            
            # 4. Granularidad: Una orden puede tener entre 1 y 4 productos (líneas de transacción)
            num_lines = random.randint(1, 4)
            # Evitamos que compre el mismo producto dos veces en la misma orden
            order_products = random.sample(product_records, num_lines)
            
            for prod in order_products:
                sales_lines.append({
                    'transaction_id': transaction_id,
                    'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'customer_id': customer['customer_id'],
                    'product_id': prod['product_id'],
                    'store_id': store_id,
                    'quantity': random.randint(1, 5),
                    # CONSISTENCIA: Tomamos el precio real del catálogo de productos
                    'unit_price': prod['unit_price'],
                    'currency_code': currency
                })
                
        return pd.DataFrame(sales_lines)

# === PRUEBA DE LA CLASE ===
if __name__ == "__main__":
    print("Inicializando generador...")
    generator = RetailDataGenerator()
    
    print("Generando dimensiones (Stores, Products, Customers)...")
    stores = generator.generate_stores()
    products = generator.generate_products(50)
    customers = generator.generate_customers(1000)
    
    print("Generando tabla de hechos (Sales) aplicando consistencia...")
    sales = generator.generate_sales(customers, products, stores, num_orders=10000)
    
    print("\n--- RESUMEN DE DATOS GENERADOS ---")
    print(f"Tiendas: {len(stores)} registros")
    print(f"Productos: {len(products)} registros")
    print(f"Clientes: {len(customers)} registros")
    print(f"Líneas de Venta (Sales): {len(sales)} registros")
    
    print("\nEjemplo de consistencia (Primera línea de venta):")
    print(sales.iloc[0].to_dict())