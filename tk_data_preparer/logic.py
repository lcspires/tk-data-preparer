"""
tk_data_preparer.logic

Funções de limpeza, filtragem e manipulação de dados para o Tk Data Preparer.
"""

import pandas as pd

def limpar_espacos_em_colunas(df: pd.DataFrame, colunas=None):
    """
    Remove espaços extras nas colunas especificadas ou em todas, se None.
    Retorna o DataFrame modificado e o total de espaços removidos.
    """
    if colunas is None:
        colunas = df.columns.tolist()

    total_espacos = 0
    for col in colunas:
        if df[col].dtype == object:
            antes = df[col].astype(str).apply(len).sum()
            df[col] = df[col].astype(str).str.strip()
            depois = df[col].astype(str).apply(len).sum()
            total_espacos += max(0, antes - depois)
    return df, total_espacos


def remover_duplicatas(df: pd.DataFrame, coluna: str):
    """
    Remove duplicatas com base em uma coluna específica.
    Retorna o DataFrame sem duplicatas e o total de linhas removidas.
    """
    total_antes = df.shape[0]
    df = df.drop_duplicates(subset=[coluna], keep='first')
    total_removido = total_antes - df.shape[0]
    return df.copy(), total_removido


def filtrar_primeira_coluna_por_tamanho(df: pd.DataFrame, coluna: str, min_len=1):
    """
    Remove linhas em que o comprimento do valor na coluna especificada é menor que min_len.
    Retorna o DataFrame filtrado e o número de linhas removidas.
    """
    condicao = df[coluna].astype(str).str.len() >= min_len
    removidas = (~condicao).sum()
    return df[condicao].copy(), removidas
