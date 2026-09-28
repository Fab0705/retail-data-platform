import pandas as pd
from src.retail_platform.transformation.currency import normalize_currency_codes

def test_normalize_currency_codes():
    data = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'currency_code': [' usd ', 'EUR', 'pe', 'MEX '] 
        # 'pe' debe ser eliminado porque no tiene 3 letras
    })
    result = normalize_currency_codes(data, currency_col='currency_code')
    assert len(result) == 3
    assert result['currency_code'].tolist() == ['USD', 'EUR', 'MEX']