import pandas as pd
import numpy as np
from src.retail_platform.transformation.cleaning import (
    remove_duplicates,
    drop_missing_critical_keys,
    strip_whitespace
)

def test_remove_duplicates():
    data = pd.DataFrame({
        'id': [1, 1, 2],
        'value': ['A', 'A', 'B']
    })
    result = remove_duplicates(data)
    assert len(result) == 2
    assert result['id'].tolist() == [1, 2]

def test_drop_missing_critical_keys():
    data = pd.DataFrame({
        'transaction_id': ['T1', None, 'T3', np.nan],
        'amount': [100, 200, 300, 400]
    })
    result = drop_missing_critical_keys(data, critical_columns=['transaction_id'])
    assert len(result) == 2
    assert result['transaction_id'].tolist() == ['T1', 'T3']

def test_strip_whitespace():
    data = pd.DataFrame({
        'name': ['  John  ', 'Jane', '  Bob'],
        'age': [30, 25, 40] # Columna numérica para asegurar que no se rompe
    })
    result = strip_whitespace(data, text_columns=['name'])
    assert result['name'].tolist() == ['John', 'Jane', 'Bob']