#!/usr/bin/env python3
"""
Script para debug do comportamento real das funções.
Execute com: python debug_behavior.py
"""

import pandas as pd
import numpy as np
import sys
import os

# Adiciona o caminho do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from tk_data_preparer.core.cleaning import CleanConfig, clean_columns
    from tk_data_preparer.core.filtering import FilterConfig, filter_by_length, drop_na_rows
    from tk_data_preparer.core.deduplication import DedupConfig, remove_duplicates
    from tk_data_preparer.core.pipeline import DataPreparationPipeline, PipelineConfig
    
    print("Módulos importados com sucesso!")
    
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de que está executando da pasta raiz do projeto")
    sys.exit(1)

def debug_empty_to_na():
    """Debug do comportamento do empty_to_na"""
    print("=== DEBUG empty_to_na ===")
    empty_data = pd.DataFrame({
        'text': ['', '   ', 'valid', None, np.nan]
    })
    print("Input:", [repr(x) for x in empty_data['text'].tolist()])
    print("Input types:", [type(x) for x in empty_data['text'].tolist()])

    config = CleanConfig(empty_to_na=True)
    result, metrics = clean_columns(empty_data, config=config)
    
    print("Output:", [repr(x) for x in result['text'].tolist()])
    print("Empty to NA count:", metrics['empty_strings_to_na'])
    print("Metrics:", metrics)
    print()

def debug_filtering():
    """Debug do comportamento do filtering"""
    print("=== DEBUG filtering ===")
    sample_data = pd.DataFrame({
        'name': ['João', 'Maria', 'Ana', 'Pedro', None, 'Lu'],
        'age': [25, 30, 28, 35, 40, 22]
    })
    print("Input names:", [repr(x) for x in sample_data['name'].tolist()])

    config = FilterConfig(min_length=3, drop_na=True)
    result, metrics = filter_by_length(sample_data, 'name', config)
    
    print("Output names:", [repr(x) for x in result['name'].tolist()])
    print("NA count in output:", result['name'].isna().sum())
    print("Removed rows:", metrics['removed_rows'])
    print("Filter metrics:", metrics)
    print()

def debug_pipeline():
    """Debug do comportamento do pipeline completo"""
    print("=== DEBUG pipeline ===")
    pipeline_data = pd.DataFrame({
        'name': ['  joão  ', 'MARIA', '  joão  ', 'ana', None, 'lu'],
        'email': ['JOÃO@EMAIL.COM', 'maria@email.com', 'joão@email.com', 'ana@email.com', None, 'lu@email.com'],
        'age': [25, 30, 25, 28, 35, 22]
    })
    
    print("Input names:", [repr(x) for x in pipeline_data['name'].tolist()])

    config = PipelineConfig(
        cleaning=CleanConfig(strip=True, collapse_whitespace=True, case='lower'),
        filtering=FilterConfig(min_length=3, drop_na=True),
        deduplication=DedupConfig(keep='first', case_sensitive=False)
    )

    pipeline = DataPreparationPipeline(config)
    result = pipeline.run(pipeline_data, 'name', columns_to_clean=['name', 'email'])
    
    print("Final names:", [repr(x) for x in result.dataframe['name'].tolist()])
    print("Final shape:", result.dataframe.shape)
    print("All metrics:")
    for step, metrics in result.metrics.items():
        print(f"  {step}: {metrics}")
    print()

def debug_filtering_step_by_step():
    """Debug detalhado do filtering"""
    print("=== DEBUG FILTERING STEP BY STEP ===")
    sample_data = pd.DataFrame({
        'name': ['João', 'Maria', 'Ana', 'Pedro', None, 'Lu'],
        'age': [25, 30, 28, 35, 40, 22]
    })
    
    print("Original data:")
    print(sample_data)
    print()
    
    # Test drop_na=False
    print("--- Testing drop_na=False ---")
    config_false = FilterConfig(min_length=3, drop_na=False)
    result_false, metrics_false = filter_by_length(sample_data, 'name', config_false)
    print("Result with drop_na=False:")
    print(result_false)
    print("Metrics:", metrics_false)
    print()
    
    # Test drop_na=True  
    print("--- Testing drop_na=True ---")
    config_true = FilterConfig(min_length=3, drop_na=True)
    result_true, metrics_true = filter_by_length(sample_data, 'name', config_true)
    print("Result with drop_na=True:")
    print(result_true)
    print("Metrics:", metrics_true)
    print()

if __name__ == "__main__":
    print("🔍 Iniciando debug do comportamento...")
    print()
    
    debug_empty_to_na()
    debug_filtering()
    debug_filtering_step_by_step()
    debug_pipeline()
    
    print("Debug completo!")