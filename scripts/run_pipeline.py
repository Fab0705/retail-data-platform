import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# 1. Asegurar que Python encuentre el paquete 'src'
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# 2. Importar nuestros módulos de transformación validados
from src.retail_platform.transformation import (
    cleaning, 
    normalization, 
    business_rules, 
    currency
)

def main():
    print("Iniciando Pipeline de Transformación de Datos...\n")
    
    # 3. Definir rutas (usando la fecha actual como partición)
    today_str = datetime.now().strftime('%Y-%m-%d')
    raw_dir = project_root / 'data' / 'raw' / 'retail' / today_str
    processed_dir = project_root / 'data' / 'processed' / 'retail' / today_str
    
    # Crear la carpeta de procesados si no existe
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"-> Leyendo datos crudos desde: data/raw/retail/{today_str}/")
    try:
        customers = pd.read_csv(raw_dir / 'customers.csv')
        products = pd.read_csv(raw_dir / 'products.csv')
        stores = pd.read_csv(raw_dir / 'stores.csv')
        sales = pd.read_csv(raw_dir / 'sales.csv')
    except FileNotFoundError as e:
        print(f"Error: No se encontraron los archivos crudos. Ejecuta generate_data.py primero.\n{e}")
        return

    # 4. APLICAR TRANSFORMACIONES
    
    print("-> Limpiando y normalizando Customers...")
    customers = cleaning.remove_duplicates(customers, subset=['customer_id'])
    customers = normalization.standardize_text_case(customers, columns=['country_code'], case='upper')

    print("-> Limpiando y validando Products...")
    products = cleaning.remove_duplicates(products, subset=['product_id'])
    products = business_rules.enforce_valid_prices(products, price_col='unit_price')

    print("-> Limpiando y normalizando Stores...")
    stores = cleaning.remove_duplicates(stores, subset=['store_id'])
    stores = normalization.standardize_text_case(stores, columns=['country_code'], case='upper')

    print("-> Aplicando reglas de negocio completas a Sales...")
    sales = cleaning.remove_duplicates(sales)
    sales = cleaning.drop_missing_critical_keys(sales, critical_columns=['transaction_id', 'customer_id', 'product_id', 'store_id'])
    sales = business_rules.enforce_positive_quantities(sales, quantity_col='quantity')
    sales = business_rules.enforce_valid_prices(sales, price_col='unit_price')
    sales = currency.normalize_currency_codes(sales, currency_col='currency_code')

    # 5. GUARDAR DATOS PROCESADOS
    print(f"\n-> Guardando datos procesados listos para el Warehouse en: data/processed/retail/{today_str}/")
    customers.to_csv(processed_dir / 'customers.csv', index=False)
    products.to_csv(processed_dir / 'products.csv', index=False)
    stores.to_csv(processed_dir / 'stores.csv', index=False)
    sales.to_csv(processed_dir / 'sales.csv', index=False)

    print("\n¡Pipeline de transformación completado con éxito!")
    print(f" - Clientes procesados: {len(customers)}")
    print(f" - Productos procesados: {len(products)}")
    print(f" - Tiendas procesadas: {len(stores)}")
    print(f" - Ventas validadas: {len(sales)}")

if __name__ == "__main__":
    main()