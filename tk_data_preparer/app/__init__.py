"""
Tkinter GUI application for tk-data-preparer.

Provides modern, modular interface for data preparation pipeline.
"""

# ✅ REMOVIDA a importação circular que causava o problema
# from .main import TkDataPreparerApp, main

# ✅ Definimos apenas o que será exportado quando alguém fizer:
# from tk_data_preparer.app import *
__all__ = [
    'TkDataPreparerApp',
    'main',
    'FileLoaderPanel', 
    'ColumnEditorPanel',
    'ConfigPanel',
    'PreviewPanel',
    'MetricsDisplay',
    'FileService',
    'AppState',
    'PipelineService',
    'ToolTip',
    'apply_theme'
]

# ✅ Para manter acessibilidade, podemos definir imports opcionais
# que só serão resolvidos quando realmente usados
def __getattr__(name):
    """Lazy imports para evitar circularidade."""
    if name == 'TkDataPreparerApp':
        from .main import TkDataPreparerApp
        return TkDataPreparerApp
    elif name == 'main':
        from .main import main
        return main
    elif name == 'FileLoaderPanel':
        from .components import FileLoaderPanel
        return FileLoaderPanel
    elif name == 'ColumnEditorPanel':
        from .components import ColumnEditorPanel
        return ColumnEditorPanel
    elif name == 'ConfigPanel':
        from .components import ConfigPanel
        return ConfigPanel
    elif name == 'PreviewPanel':
        from .components import PreviewPanel
        return PreviewPanel
    elif name == 'MetricsDisplay':
        from .components import MetricsDisplay
        return MetricsDisplay
    elif name == 'FileService':
        from .services import FileService
        return FileService
    elif name == 'AppState':
        from .services import AppState
        return AppState
    elif name == 'PipelineService':
        from .services import PipelineService
        return PipelineService
    elif name == 'ToolTip':
        from .utils import ToolTip
        return ToolTip
    elif name == 'apply_theme':
        from .utils import apply_theme
        return apply_theme
    else:
        raise AttributeError(f"module 'tk_data_preparer.app' has no attribute '{name}'")