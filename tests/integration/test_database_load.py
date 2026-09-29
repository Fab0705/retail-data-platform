import pytest
import psycopg2
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
import sys
from pathlib import Path

# Asegurar que pytest encuentre nuestro código
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.retail_platform.loading.connection import DatabaseConnection

@pytest.fixture(scope="module")
def db_conn():
    """Configura la conexión a la base de datos para todas las pruebas."""
    manager = DatabaseConnection()
    conn = manager.connect()
    yield conn
    # Teardown: Al terminar las pruebas, hacemos rollback para no dejar basura en la BD
    conn.rollback() 
    manager.close()

def test_prevent_duplicate_world_bank_observation(db_conn):
    """
    Responde a: Can the same World Bank observation be inserted twice?
    Prueba que la restricción UNIQUE en fact_economy funciona correctamente.
    """
    cursor = db_conn.cursor()
    
    # 1. Insertamos un registro de prueba válido
    query = """
    INSERT INTO retail.fact_economy (country_code, indicator_code, year, value) 
    VALUES ('ZZZ', 'TEST.INDICATOR', 2099, 150.5)
    """
    cursor.execute(query)
    
    # 2. Intentamos insertar EXACTAMENTE el mismo registro (sin usar ON CONFLICT)
    # Esperamos que PostgreSQL lance un error de violación de unicidad
    with pytest.raises(UniqueViolation):
        cursor.execute(query)
        
    db_conn.rollback() # Limpiamos la transacción fallida para la siguiente prueba

def test_prevent_duplicate_customer(db_conn):
    """
    Asegura que no podamos tener dos clientes con el mismo ID natural.
    """
    cursor = db_conn.cursor()
    
    query = """
    INSERT INTO retail.dim_customer (customer_id, customer_name, gender, country_code, customer_segment)
    VALUES ('CUST-TEST', 'Test User', 'M', 'PER', 'Standard')
    """
    cursor.execute(query)
    
    with pytest.raises(UniqueViolation):
        cursor.execute(query)
        
    db_conn.rollback()

def test_fact_references_nonexistent_customer(db_conn):
    """
    Responde a: Can a fact reference a nonexistent customer?
    Prueba que las llaves foráneas (Foreign Keys) protegen la integridad referencial.
    """
    cursor = db_conn.cursor()
    
    # Intentamos insertar una venta vinculada al customer_key = 9999999 (que no existe)
    query = """
    INSERT INTO retail.fact_sales (transaction_id, date_key, customer_key, product_key, store_key, currency_key, quantity, unit_price)
    VALUES ('TRX-TEST', 20260928, 9999999, 1, 1, 1, 5, 10.0)
    """
    
    # Si creaste Foreign Keys en la Fase 7, esto lanzará un ForeignKeyViolation.
    # (Si la prueba falla, significa que te falta agregar la restricción FOREIGN KEY en tu SQL).
    with pytest.raises(ForeignKeyViolation):
        cursor.execute(query)
        
    db_conn.rollback()