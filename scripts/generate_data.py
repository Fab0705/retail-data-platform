import sys
import yaml
import json
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.retail_platform.extraction.sales_generator import RetailDataGenerator
from src.retail_platform.extraction.world_bank import WorldBankClient

def main():
    print("Iniciando Fase 11: Raw Storage & Extracción Completa...\n")
    
    # 1. Definir estructura de carpetas (Particionadas por fecha)
    today_str = datetime.now().strftime('%Y-%m-%d')
    retail_raw_dir = project_root / 'data' / 'raw' / 'retail' / today_str
    wb_raw_dir = project_root / 'data' / 'raw' / 'world_bank' / today_str
    
    retail_raw_dir.mkdir(parents=True, exist_ok=True)
    wb_raw_dir.mkdir(parents=True, exist_ok=True)
    
    # --- EXTRACCIÓN RETAIL ---
    print("1. Extrayendo datos sintéticos de Retail...")
    generator = RetailDataGenerator()
    stores_df = generator.generate_stores()
    products_df = generator.generate_products(num_products=50)
    customers_df = generator.generate_customers(num_customers=1000)
    sales_df = generator.generate_sales(customers_df, products_df, stores_df, num_orders=10000)
    
    # Guardado físico en Raw Storage particionado
    stores_df.to_csv(retail_raw_dir / 'stores.csv', index=False)
    products_df.to_csv(retail_raw_dir / 'products.csv', index=False)
    customers_df.to_csv(retail_raw_dir / 'customers.csv', index=False)
    sales_df.to_csv(retail_raw_dir / 'sales.csv', index=False)
    print(f"   ✓ Guardados exitosamente en: {retail_raw_dir}")
    
    # --- EXTRACCIÓN BANCO MUNDIAL ---
    print("\n2. Extrayendo indicadores de la API del Banco Mundial...")
    
    # Leer configuración desde sources.yaml
    with open(project_root / 'config' / 'sources.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    wb_config = config['sources']['world_bank']
    countries = wb_config['countries']
    indicators = [ind['code'] for ind in wb_config['indicators']]
    
    # Usar el cliente actualizado con paginación
    wb_client = WorldBankClient()
    try:
        raw_wb_data = wb_client.get_indicators(
            countries=countries,
            indicators=indicators,
            start_year=wb_config['start_year'],
            end_year=wb_config['end_year']
        )
        
        # Guardado físico en Raw Storage particionado como JSON
        wb_file_path = wb_raw_dir / 'indicators.json'
        with open(wb_file_path, 'w', encoding='utf-8') as f:
            json.dump(raw_wb_data, f, indent=2, ensure_ascii=False)
            
        print(f"   ✓ {len(raw_wb_data)} observaciones guardadas exitosamente en: {wb_file_path}")
    except Exception as e:
        print(f"   ! Error al extraer Banco Mundial: {e}")

    print("\n¡Pipeline de Extracción RAW completado!")

if __name__ == "__main__":
    main()