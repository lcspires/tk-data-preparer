# tests/test_deduplication.py
import pytest
import pandas as pd
import numpy as np
from tk_data_preparer.core.deduplication import DedupConfig, remove_duplicates

class TestDeduplication:
    def setup_method(self):
        self.duplicate_data = pd.DataFrame({
            'email': ['joao@email.com', 'MARIA@EMAIL.COM', 'joao@email.com', 'ana@email.com', 'maria@email.com'],
            'name': ['João', 'Maria', 'João Silva', 'Ana', 'Maria Santos']
        })
    
    def test_case_sensitive_deduplication(self):
        """Test case-sensitive deduplication"""
        config = DedupConfig(keep='first', case_sensitive=True)
        result, metrics = remove_duplicates(self.duplicate_data, 'email', config)
        
        # Should remove exact duplicates only
        assert len(result) == 4  # joao@email.com appears twice (case different)
        assert metrics['removed_duplicates'] == 1
    
    def test_case_insensitive_deduplication(self):
        """Test case-insensitive deduplication"""
        config = DedupConfig(keep='first', case_sensitive=False)
        result, metrics = remove_duplicates(self.duplicate_data, 'email', config)
        
        # Should remove case variations
        assert len(result) == 3  # MARIA@EMAIL.COM and maria@email.com are duplicates
        assert metrics['removed_duplicates'] == 2
    
    def test_keep_strategies(self):
        """Test different keep strategies"""
        data = pd.DataFrame({
            'email': ['a@b.com', 'a@b.com', 'a@b.com'],
            'value': [1, 2, 3]
        })
        
        # Test keep first
        config = DedupConfig(keep='first')
        result, metrics = remove_duplicates(data, 'email', config)
        assert result['value'].iloc[0] == 1
        
        # Test keep last
        config = DedupConfig(keep='last')
        result, metrics = remove_duplicates(data, 'email', config)
        assert result['value'].iloc[0] == 3