import pandas as pd

class BusinessValidator:
    @staticmethod
    def check_positive_value(df: pd.DataFrame, entity_name: str, column: str, level: str = "WARNING"):
        """Valida reglas comerciales: cantidades y precios no pueden ser negativos."""
        if column in df.columns:
            invalid = (df[column] < 0).sum()
            if invalid > 0:
                msg = f"[{entity_name}] {invalid} registros tienen '{column}' negativo."
                print(f"  [{level}] {msg}")
                if level == "ERROR":
                    raise ValueError(f"Fallo de regla de negocio: {msg}")
            else:
                print(f"  [INFO] {entity_name}: Regla comercial '{column} >= 0' validada.")

    @staticmethod
    def check_allowed_values(df: pd.DataFrame, entity_name: str, column: str, allowed_values: list, level: str = "ERROR"):
        """Valida que una columna categórica solo contenga valores autorizados (ej. Códigos de país ISO)."""
        if column in df.columns:
            invalid_mask = ~df[column].isin(allowed_values)
            invalid_count = invalid_mask.sum()
            if invalid_count > 0:
                bad_values = df.loc[invalid_mask, column].unique().tolist()
                msg = f"[{entity_name}] {invalid_count} registros tienen valores no permitidos en '{column}': {bad_values}"
                print(f"  [{level}] {msg}")
                if level == "ERROR":
                    raise ValueError(f"Fallo de regla de negocio: {msg}")
            else:
                print(f"  [INFO] {entity_name}: Valores permitidos en '{column}' validados.")