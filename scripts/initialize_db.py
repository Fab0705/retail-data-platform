import psycopg2
from pathlib import Path
import traceback

DB_CONFIG = {
    "dbname": "retail_dw",
    "user": "retail_user",
    "password": "retail_password",
    "host": "127.0.0.1",
    "port": "5433"
}

def execute_sql_file(cursor, filepath):
    """Lee y ejecuta un archivo SQL. 'replace' evita cualquier error de decodificación."""
    print(f"Ejecutando: {filepath.name}...", flush=True)
    with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
        sql_content = file.read()
    cursor.execute(sql_content)

def main():
    # Obtener la ruta absoluta de la carpeta sql/
    base_dir = Path(__file__).resolve().parent.parent / 'sql'
    
    # Definir el orden estricto de ejecución
    folders_in_order = [
        "00_database",
        "01_staging",
        "02_dimensions",
        "03_facts"
    ]

    print("Conectando a PostgreSQL en Docker...", flush=True)
    
    # Quitamos el bloque try/except para que, si falla, veamos la línea EXACTA del error.
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True  
    cursor = conn.cursor()

    for folder in folders_in_order:
        folder_path = base_dir / folder
        if not folder_path.exists():
            continue
            
        sql_files = sorted(folder_path.glob("*.sql"))
        for sql_file in sql_files:
            execute_sql_file(cursor, sql_file)

    print("\n¡Base de datos inicializada con éxito!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()