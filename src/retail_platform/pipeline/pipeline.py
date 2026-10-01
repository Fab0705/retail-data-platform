import pandas as pd
from datetime import datetime
from pathlib import Path
import yaml

# Importar todos nuestros módulos modulares
from src.retail_platform.extraction.world_bank import WorldBankClient
from src.retail_platform.extraction.sales_generator import RetailDataGenerator
from src.retail_platform.transformation import cleaning, normalization, business_rules, currency
from src.retail_platform.validation import DataValidator
from src.retail_platform.loading.connection import DatabaseConnection
from src.retail_platform.loading.staging_loader import StagingLoader
from src.retail_platform.loading.dimension_loader import DimensionLoader
from src.retail_platform.loading.fact_loader import FactLoader
from src.retail_platform.monitoring.metrics import PipelineMetrics

class MasterPipeline:
    def __init__(self, project_root: Path):
        self.root = project_root
        self.metrics = PipelineMetrics()
        self.today = datetime.now().strftime('%Y-%m-%d')
        
        # Rutas de almacenamiento
        self.raw_dir = self.root / 'data' / 'raw' / 'retail' / self.today
        self.processed_dir = self.root / 'data' / 'processed' / 'retail' / self.today
        
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        try:
            print(f"Iniciando Pipeline... [Run ID: {self.metrics.run_id}]")
            
            # --- 1. EXTRACTION ---
            print("-> 1. Extrayendo datos...")
            generator = RetailDataGenerator()
            customers = generator.generate_customers(1000)
            products = generator.generate_products(50)
            stores = generator.generate_stores()
            sales = generator.generate_sales(customers, products, stores, 10000)
            
            self.metrics.extraction['sales'] = len(sales)
            # (Aquí se agregaría la extracción del Banco Mundial)

            # --- 1.5: Extracción Banco Mundial ---
            print("-> 1.5 Extrayendo indicadores del Banco Mundial...")
            with open(self.root / 'config' / 'sources.yaml', 'r') as file:
                wb_config = yaml.safe_load(file)['sources']['world_bank']
            
            wb_client = WorldBankClient()
            wb_data = wb_client.get_indicators(
                countries=wb_config['countries'],
                indicators=[ind['code'] for ind in wb_config['indicators']],
                start_year=wb_config['start_year'],
                end_year=wb_config['end_year']
            )
            self.metrics.extraction['world_bank'] = len(wb_data)

            # Preparar DataFrame del Banco Mundial
            wb_df = pd.json_normalize(wb_data)
            wb_df = wb_df.rename(columns={
                'countryiso3code': 'country_code',
                'indicator.id': 'indicator_code',
                'date': 'year'
            })[['country_code', 'indicator_code', 'year', 'value']]
            # Limpiar años sin datos (común en el Banco Mundial)
            wb_df = wb_df.dropna(subset=['value'])

            # --- 2. TRANSFORMATION & VALIDATION ---
            print("-> 2. Transformando y validando...")
            # Limpieza básica
            sales_clean = cleaning.remove_duplicates(sales)
            sales_clean = cleaning.drop_missing_critical_keys(sales_clean, ['transaction_id'])
            
            # Calidad de datos
            validator = DataValidator()

            # 1. Validas Estructura primero
            validator.schema.validate_required_columns(
                sales_clean, "Sales", ["transaction_id", "product_id", "quantity", "unit_price"]
            )

            # 2. Validas Integridad Técnica
            validator.quality.check_not_null(sales_clean, "Sales", "transaction_id")
            validator.quality.check_unique(sales_clean, "Sales", ["transaction_id", "product_id"])

            # 3. Validas Reglas de Negocio
            validator.business.check_positive_value(sales_clean, "Sales", "unit_price", level="WARNING")
            validator.business.check_allowed_values(
                customers, "Customers", "country_code", allowed_values=['PER', 'BRA', 'CHL', 'COL', 'MEX']
            )
            
            # Rastrear registros rechazados vs pasados
            self.metrics.validation['passed'] = len(sales_clean)
            self.metrics.validation['rejected'] = len(sales) - len(sales_clean)

            # --- 3. LOADING ---
            print("-> 3. Cargando al Data Warehouse...")
            db_conn = DatabaseConnection()
            try:
                staging = StagingLoader(db_conn)
                dimensions = DimensionLoader(db_conn)
                facts = FactLoader(db_conn)

                # Staging
                staging.load_table(customers, 'customers', customers.columns.tolist())
                staging.load_table(sales_clean, 'sales', sales_clean.columns.tolist())
                staging.load_table(wb_df, 'world_bank', wb_df.columns.tolist())
                # Dimensions & Facts
                dimensions.upsert_customers()
                facts.upsert_sales()
                facts.upsert_economic_facts()

                # Registrar métricas de carga
                self.metrics.loading['dimensions'] = len(customers)
                self.metrics.loading['sales'] = len(sales_clean)
                self.metrics.loading['economic_facts'] = len(wb_df)

            except Exception as e:
                db_conn.conn.rollback()
                raise e
            finally:
                db_conn.close()

            # --- 4. RECORD EXECUTION ---
            self.metrics.end_run(status="SUCCESS")
            
        except Exception as e:
            print(f"\n[!] Error crítico en el pipeline: {e}")
            self.metrics.end_run(status="FAILED")
            
        finally:
            # Imprimir reporte de monitoreo al finalizar (Fase 18)
            self.metrics.print_summary()