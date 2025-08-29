"""
Tk Data Preparer

A Tkinter-based tool for cleaning, preprocessing, and exporting tabular data.
"""

from .logic import (
    limpar_espacos_em_colunas,
    remover_duplicatas,
    filtrar_primeira_coluna_por_tamanho,
)
from .tooltip import ToolTip
from .app import UnifiedApp

__all__ = [
    "limpar_espacos_em_colunas",
    "remover_duplicatas",
    "filtrar_primeira_coluna_por_tamanho",
    "ToolTip",
    "UnifiedApp",
]

__version__ = "0.2.0"
