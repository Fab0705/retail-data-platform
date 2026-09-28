import pandas as pd
from src.retail_platform.transformation.normalization import (
    standardize_dates,
    standardize_text_case
)

def test_standardize_dates():
    data = pd.DataFrame({
        'date': ['12/31/2024', '2024-01-15', '15-02-2024']
    })
    # pandas to_datetime con dayfirst=False por defecto interpretará 15-02-2024 
    # pero para la prueba simplificada, confiamos en la capacidad deductiva de pandas.
    result = standardize_dates(data, date_columns=['date'])
    assert result['date'].tolist() == ['2024-12-31', '2024-01-15', '2024-02-15']

def test_standardize_text_case():
    data = pd.DataFrame({
        'country_code': ['per', 'Bra', 'CHL']
    })
    result_upper = standardize_text_case(data, columns=['country_code'], case='upper')
    assert result_upper['country_code'].tolist() == ['PER', 'BRA', 'CHL']
    
    result_lower = standardize_text_case(data, columns=['country_code'], case='lower')
    assert result_lower['country_code'].tolist() == ['per', 'bra', 'chl']