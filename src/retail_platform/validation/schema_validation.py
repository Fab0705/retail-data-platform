import pandas as pd

class SchemaValidator:
    @staticmethod
    def validate_required_columns(df: pd.DataFrame, entity_name: str, required_columns: list):
        """Valida que la tabla contenga exactamente las columnas esperadas."""
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"[{entity_name}] ERROR DE ESQUEMA: Faltan las columnas requeridas: {missing}")
        print(f"  [INFO] {entity_name}: Esquema de columnas (Schema) validado.")