import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# 1. Asegurar que Python encuentre el paquete 'src'
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.retail_platform.loading.connection import DatabaseConnection
from src.retail_platform.loading.staging_loader import StagingLoader
from src.retail_platform.loading.dimension_loader import DimensionLoader
from src.retail_platform.loading.fact_loader import FactLoader
from src.retail_platform.quality.validator import DataQualityValidator

def main():
    print("Iniciando Fase Final: Carga Incremental al Data Warehouse...\n")
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    processed_dir = project_root / 'data' / 'processed' / 'retail' / today_str
    
    # 1. LECTURA DE DATOS PROCESADOS
    print("1. Leyendo datos procesados (Capa Silver)...")
    try:
        customers = pd.read_csv(processed_dir / 'customers.csv')
        sales = pd.read_csv(processed_dir / 'sales.csv')
        # Puedes agregar products y stores aquí cuando crees sus tablas en Staging
    except FileNotFoundError:
        print("Error: No se encontraron los archivos procesados. Ejecuta run_pipeline.py primero.")
        return

    # 2. FASE 13: DATA QUALITY (Última barrera antes de la base de datos)
    print("2. Ejecutando validaciones de Calidad de Datos (Fase 13)...")
    validator = DataQualityValidator()
    
    validator.validate_not_null(customers, "Customers", "customer_id")
    validator.validate_unique(customers, "Customers", ["customer_id"])
    
    validator.validate_not_null(sales, "Sales", "transaction_id")
    validator.validate_greater_than_or_equal_zero(sales, "Sales", "unit_price", level="WARNING")
    
    print("  ✓ Todas las pruebas de calidad superadas.")

    # 3. FASE 14 & 15: CARGA (Loading & Upserts)
    print("\n3. Iniciando conexión a PostgreSQL en Docker...")
    db_conn = DatabaseConnection()
    
    try:
        staging = StagingLoader(db_conn)
        dimensions = DimensionLoader(db_conn)
        facts = FactLoader(db_conn)

        # A. Carga masiva y rápida al esquema Staging
        print("\n4. Cargando datos a la capa Staging...")
        staging.load_table(customers, 'customers', [
            'customer_id', 'customer_name', 'gender', 'country_code', 'customer_segment', 'registration_date'
        ])
        staging.load_table(sales, 'sales', [
            'transaction_id', 'transaction_date', 'customer_id', 'product_id', 'store_id', 'quantity', 'unit_price', 'currency_code'
        ])

        # B. Upserts a Dimensiones (Esquema Retail)
        print("\n5. Actualizando Dimensiones (Fase 15: Upserts)...")
        dimensions.upsert_customers()

        # C. Upserts a Hechos (Resolviendo Surrogate Keys vía SQL)
        print("\n6. Actualizando Hechos (Resolviendo Surrogate Keys)...")
        facts.upsert_sales()

        print("\n¡Pipeline de Carga completado con éxito! Tu Data Warehouse está actualizado.")
        
    except Exception as e:
        print(f"\nError crítico durante la carga: {e}")
        if db_conn.conn:
            db_conn.conn.rollback() 
            print("Se detectó un fallo. Se aplicó ROLLBACK para proteger la integridad de los datos.")
    finally:
        db_conn.close()

if __name__ == "__main__":
    main()