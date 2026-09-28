import pandas as pd
from src.retail_platform.transformation.business_rules import (
    enforce_positive_quantities,
    enforce_valid_prices
)

def test_enforce_positive_quantities():
    data = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'quantity': [10, 0, -5, 3]
    })
    result = enforce_positive_quantities(data, quantity_col='quantity')
    assert len(result) == 2
    assert result['quantity'].tolist() == [10, 3]

def test_enforce_valid_prices():
    data = pd.DataFrame({
        'id': [1, 2, 3],
        'unit_price': [15.50, -2.00, 0.00] # 0 es válido (ej. promoción 100% descuento)
    })
    result = enforce_valid_prices(data, price_col='unit_price')
    assert len(result) == 2
    assert result['unit_price'].tolist() == [15.50, 0.00]