import pandas as pd
from psycopg2.extras import execute_values

class StagingLoader:
    def __init__(self, connection_manager):
        self.conn = connection_manager.connect()

    def load_table(self, df: pd.DataFrame, table_name: str, columns: list):
        """Carga cruda y rápida usando execute_values"""
        cursor = self.conn.cursor()
        # El staging siempre se vacía antes de cada carga
        cursor.execute(f"TRUNCATE TABLE staging.{table_name};")
        
        query = f"INSERT INTO staging.{table_name} ({', '.join(columns)}) VALUES %s"
        # Convertir DataFrame a lista de tuplas para inserción masiva
        values = [tuple(x) for x in df[columns].to_numpy()]
        
        execute_values(cursor, query, values)
        self.conn.commit()
        cursor.close()
        print(f"  ✓ {len(df)} registros cargados en staging.{table_name}")