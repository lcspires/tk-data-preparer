"""
Logic functions for data preparation in the tk_data_preparer app.

Includes:
- Removing extra spaces from all string columns.
- Filtering rows based on minimum character length in the first column.
- Removing duplicates based on the first column.
"""

import pandas as pd


def limpar_espacos_em_colunas(df: pd.DataFrame, colunas: list):
    """
    Removes extra spaces in the specified columns of the DataFrame.
    Returns the cleaned DataFrame and the total number of spaces removed.
    """
    total_espacos_removidos = 0
    for col in colunas:
        if df[col].dtype == object:  # Process only string columns
            original = df[col].astype(str)
            limpo = original.str.strip().str.replace(r"\s+", " ", regex=True)
            espacos_removidos = (original.str.len() - limpo.str.len()).sum()
            total_espacos_removidos += espacos_removidos
            df[col] = limpo
    return df, total_espacos_removidos


def filtrar_primeira_coluna_por_tamanho(df: pd.DataFrame, primeira_coluna: str, min_len: int = 6):
    """
    Removes rows where the first column has fewer characters than min_len.
    Returns the filtered DataFrame and the number of rows removed.
    """
    tamanho_anterior = len(df)
    df = df[df[primeira_coluna].astype(str).str.len() >= min_len]
    linhas_removidas = tamanho_anterior - len(df)
    return df, linhas_removidas


def remover_duplicatas(df: pd.DataFrame, primeira_coluna: str):
    """
    Removes duplicate rows based on the first column.
    Keeps the first occurrence and discards the others.
    Returns the DataFrame and the number of duplicates removed.
    """
    tamanho_anterior = len(df)
    df = df.drop_duplicates(subset=[primeira_coluna], keep="first")
    duplicatas_removidas = tamanho_anterior - len(df)
    return df, duplicatas_removidas
