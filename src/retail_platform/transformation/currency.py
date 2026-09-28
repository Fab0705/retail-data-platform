import pandas as pd

def normalize_currency_codes(df: pd.DataFrame, currency_col: str = 'currency_code') -> pd.DataFrame:
    """Estandariza los códigos de moneda al formato ISO 4217 de 3 letras en mayúscula."""
    if currency_col in df.columns:
        df[currency_col] = df[currency_col].str.upper().str.strip()
        # Validación de longitud: los códigos ISO siempre tienen 3 letras
        df = df[df[currency_col].str.len() == 3]
    return df