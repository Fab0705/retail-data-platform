import pandas as pd

def enforce_positive_quantities(df: pd.DataFrame, quantity_col: str = 'quantity') -> pd.DataFrame:
    """Filtra los registros donde la cantidad comprada es 0 o negativa."""
    if quantity_col in df.columns:
        df = df[df[quantity_col] > 0]
    return df

def enforce_valid_prices(df: pd.DataFrame, price_col: str = 'unit_price') -> pd.DataFrame:
    """Filtra los registros donde el precio es negativo (lo cual no tiene sentido comercial)."""
    if price_col in df.columns:
        df = df[df[price_col] >= 0]
    return df