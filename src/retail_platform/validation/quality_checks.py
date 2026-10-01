import pandas as pd

class QualityValidator:
    @staticmethod
    def check_not_null(df: pd.DataFrame, entity_name: str, column: str, level: str = "ERROR"):
        """Valida la ausencia de nulos en llaves o campos críticos."""
        if column not in df.columns:
            return
            
        nulls = df[column].isnull().sum()
        if nulls > 0:
            msg = f"[{entity_name}] {nulls} registros tienen '{column}' nulo."
            print(f"  [{level}] {msg}")
            if level == "ERROR":
                raise ValueError(f"Fallo de calidad crítico: {msg}")
        else:
            print(f"  [INFO] {entity_name}: Calidad de '{column}' validada (0 nulos).")

    @staticmethod
    def check_unique(df: pd.DataFrame, entity_name: str, columns: list, level: str = "ERROR"):
        """Valida que no existan registros duplicados basados en sus llaves primarias/compuestas."""
        dupes = df.duplicated(subset=columns).sum()
        if dupes > 0:
            msg = f"[{entity_name}] {dupes} registros duplicados basados en {columns}."
            print(f"  [{level}] {msg}")
            if level == "ERROR":
                raise ValueError(f"Fallo de calidad crítico: {msg}")
        else:
            print(f"  [INFO] {entity_name}: Unicidad de {columns} validada.")