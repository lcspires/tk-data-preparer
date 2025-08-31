"""
tk-data-preparer - Ferramenta para preparação de dados com interface gráfica.
"""

__version__ = "0.1.0"

# Exportar componentes principais para facilitar imports
from .core import (
    CleanConfig, FilterConfig, DedupConfig, PipelineConfig,
    clean_columns, filter_by_length, remove_duplicates,
    DataPreparationPipeline, PipelineResult,
    AppConfig, DEFAULT_CONFIG, PRESET_CONFIGS
)

__all__ = [
    'CleanConfig',
    'FilterConfig',
    'DedupConfig', 
    'PipelineConfig',
    'clean_columns',
    'filter_by_length',
    'remove_duplicates',
    'DataPreparationPipeline',
    'PipelineResult',
    'AppConfig',
    'DEFAULT_CONFIG',
    'PRESET_CONFIGS'
]