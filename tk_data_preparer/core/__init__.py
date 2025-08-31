"""
Módulo core com funcionalidades principais de processamento de dados.
"""

from .cleaning import CleanConfig, clean_columns
from .filtering import FilterConfig, filter_by_length, drop_na_rows
from .deduplication import DedupConfig, remove_duplicates
from .pipeline import PipelineConfig, DataPreparationPipeline, PipelineResult
from .config import AppConfig, DEFAULT_CONFIG, PRESET_CONFIGS

__all__ = [
    'CleanConfig',
    'clean_columns',
    'FilterConfig', 
    'filter_by_length',
    'drop_na_rows',
    'DedupConfig',
    'remove_duplicates',
    'PipelineConfig',
    'DataPreparationPipeline',
    'PipelineResult',
    'AppConfig',
    'DEFAULT_CONFIG',
    'PRESET_CONFIGS'
]