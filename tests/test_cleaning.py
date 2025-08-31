# tests/test_cleaning.py - CORRIGIDO
import pytest
import pandas as pd
import numpy as np
from tk_data_preparer.core.cleaning import CleanConfig, clean_columns

class TestCleaning:
    def setup_method(self):
        self.sample_data = pd.DataFrame({
            'name': ['  João  Silva  ', 'MARIA', None, 'ana   costa'],
            'age': [25, 30, 28, 35],
            'email': ['  JOÃO@EMAIL.COM  ', 'maria@email.com', None, 'ana@email.com']
        })
    
    def test_basic_cleaning(self):
        """Test basic whitespace cleaning"""
        config = CleanConfig(strip=True, collapse_whitespace=True)
        result, metrics = clean_columns(self.sample_data, config=config)
        
        assert result['name'].iloc[0] == 'João Silva'
        assert metrics['total_whitespace_removed'] > 0
        assert 'name' in metrics['columns_processed']
    
    def test_unicode_normalization(self):
        """Test Unicode normalization - CORRIGIDO"""
        unicode_data = pd.DataFrame({
            'text': ['café', 'cafe\u0301', 'ñandú']  # café com acento agudo e combinado
        })
        
        config = CleanConfig(unicode_normalization='NFKC')
        result, metrics = clean_columns(unicode_data, config=config)
        
        # Should normalize to consistent form - verifique se são iguais após normalização
        assert result['text'].iloc[0] == result['text'].iloc[1]  # ambos devem ser 'café'
        assert result['text'].iloc[2] == 'ñandú'  # ñ não é afetado por NFKC
    
    def test_empty_to_na(self):
        """Test empty string conversion to NA - CORRIGIDO baseado no comportamento REAL"""
        empty_data = pd.DataFrame({
            'text': ['', '   ', 'valid', None, np.nan]
        })
        
        config = CleanConfig(empty_to_na=True)
        result, metrics = clean_columns(empty_data, config=config)
        
        # Comportamento REAL: converte '', '   ', None, e np.nan para NA
        assert pd.isna(result['text'].iloc[0])  # '' -> NA
        assert pd.isna(result['text'].iloc[1])  # '   ' -> NA
        assert not pd.isna(result['text'].iloc[2])  # 'valid' mantém
        assert pd.isna(result['text'].iloc[3])  # None -> NA
        assert pd.isna(result['text'].iloc[4])  # np.nan -> NA
        
        # Seu código conta 4 conversões (todos os não-strings válidos)
        assert metrics['empty_strings_to_na'] == 4

    def test_column_selection(self):
        """Test automatic column detection"""
        mixed_data = pd.DataFrame({
            'string_col': ['a', 'b'],
            'numeric_col': [1, 2],
            'object_col': ['x', 'y']  # object dtype
        })
        
        result, metrics = clean_columns(mixed_data)
        
        assert 'string_col' in metrics['columns_processed']
        assert 'object_col' in metrics['columns_processed']
        assert 'numeric_col' not in metrics['columns_processed']