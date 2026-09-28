import pandas as pd

class DataQualityValidator:
    def __init__(self):
        self.logs = []

    def _log(self, level: str, message: str):
        self.logs.append(f"[{level}] {message}")
        print(f"[{level}] {message}")

    def validate_not_null(self, df: pd.DataFrame, entity_name: str, column: str, level: str = "ERROR"):
        """Valida reglas como: customer_id NOT NULL o product_id NOT NULL"""
        nulls = df[column].isnull().sum()
        if nulls > 0:
            self._log(level, f"{entity_name}: {nulls} registros tienen '{column}' nulo.")
            if level == "ERROR":
                raise ValueError(f"Fallo de calidad crítico en {entity_name}. Pipeline detenido.")

    def validate_unique(self, df: pd.DataFrame, entity_name: str, columns: list, level: str = "ERROR"):
        """Valida reglas como: store_id UNIQUE"""
        dupes = df.duplicated(subset=columns).sum()
        if dupes > 0:
            self._log(level, f"{entity_name}: {dupes} registros duplicados basados en {columns}.")
            if level == "ERROR":
                raise ValueError(f"Fallo de calidad crítico en {entity_name}. Pipeline detenido.")

    def validate_greater_than_or_equal_zero(self, df: pd.DataFrame, entity_name: str, column: str, level: str = "WARNING"):
        """Valida reglas como: unit_price >= 0"""
        invalid = (df[column] < 0).sum()
        if invalid > 0:
            self._log(level, f"{entity_name}: {invalid} registros tienen '{column}' negativo.")
            # Si es un WARNING, el pipeline continúa pero deja un registro del problema.