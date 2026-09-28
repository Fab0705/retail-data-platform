import psycopg2

class DatabaseConnection:
    """Maneja una única responsabilidad: la conexión a PostgreSQL"""
    def __init__(self):
        self.db_config = {
            "dbname": "retail_dw",
            "user": "retail_user",
            "password": "retail_password",
            "host": "127.0.0.1",
            "port": "5433" # Usamos el puerto que definimos en Docker para evitar conflictos
        }
        self.conn = None

    def connect(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(**self.db_config)
            # Autocommit en False es ideal para cargar datos: 
            # Si algo falla a la mitad, se cancela todo (Rollback).
            self.conn.autocommit = False 
        return self.conn

    def close(self):
        if self.conn is not None and not self.conn.closed:
            self.conn.close()