# tests/test_integration.py - CORRIGIDO
import pytest
import pandas as pd
from tk_data_preparer.core.cleaning import clean_columns, CleanConfig
from tk_data_preparer.core.filtering import filter_by_length, FilterConfig
from tk_data_preparer.core.deduplication import remove_duplicates, DedupConfig

def test_integration_cleaning_filtering():
    """Test integration between cleaning and filtering - CORRIGIDO"""
    data = pd.DataFrame({
        'name': ['  joão  ', '  maria  ', 'ana'],  # ana tem 3 chars, joão e maria têm mais após cleaning
        'value': [1, 2, 3]
    })
    
    # First clean - remove espaços
    cleaned, clean_metrics = clean_columns(data, config=CleanConfig(strip=True))
    
    # Then filter - min_length=3 (todos passam)
    filtered, filter_metrics = filter_by_length(
        cleaned, 'name', FilterConfig(min_length=3)
    )
    
    assert len(filtered) == 3  # todos passam: 'joão' (4), 'maria' (5), 'ana' (3)
    assert filtered['name'].iloc[0] == 'joão'  # Cleaned

def test_integration_cleaning_deduplication():
    """Test integration between cleaning and deduplication"""
    data = pd.DataFrame({
        'email': ['  JOÃO@EMAIL.COM  ', 'joão@email.com', 'MARIA@EMAIL.COM'],
        'value': [1, 2, 3]
    })
    
    # First clean
    cleaned, _ = clean_columns(data, config=CleanConfig(strip=True, case='lower'))
    
    # Then deduplicate
    deduped, dedup_metrics = remove_duplicates(
        cleaned, 'email', DedupConfig(case_sensitive=True)
    )
    
    assert len(deduped) == 2  # Duplicates removed after cleaning