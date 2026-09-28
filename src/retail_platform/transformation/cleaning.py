import pandas as pd

def remove_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """Elimina filas duplicadas exactas o basadas en columnas específicas."""
    return df.drop_duplicates(subset=subset)

def drop_missing_critical_keys(df: pd.DataFrame, critical_columns: list) -> pd.DataFrame:
    """Asegura la limpieza estructural eliminando filas sin llaves primarias/foráneas."""
    return df.dropna(subset=critical_columns)

def strip_whitespace(df: pd.DataFrame, text_columns: list) -> pd.DataFrame:
    """Limpia espacios en blanco accidentales al inicio o final de las cadenas de texto."""
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df