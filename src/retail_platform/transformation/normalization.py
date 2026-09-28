import pandas as pd

def standardize_dates(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
    """Convierte cualquier formato de fecha de origen a un estándar consistente YYYY-MM-DD."""
    for col in date_columns:
        if col in df.columns:
            # Agregamos format='mixed' para manejar múltiples formatos en la misma columna
            df[col] = pd.to_datetime(df[col], format='mixed').dt.strftime('%Y-%m-%d')
    return df

def standardize_text_case(df: pd.DataFrame, columns: list, case: str = 'upper') -> pd.DataFrame:
    """Asegura que identificadores como códigos de país sean consistentes."""
    for col in columns:
        if col in df.columns:
            if case == 'upper':
                df[col] = df[col].str.upper()
            elif case == 'lower':
                df[col] = df[col].str.lower()
    return df