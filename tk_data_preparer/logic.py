# tk_data_preparer/logic.py - Day 1 MVP

import pandas as pd

def limpar_espacos_em_colunas(df: pd.DataFrame, colunas: list):
    """
    Remove leading/trailing spaces from all string columns in the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to clean.
        colunas (list): List of columns to clean.
    
    Returns:
        pd.DataFrame: Cleaned DataFrame.
        int: Total number of spaces removed.
    """
    total_espacos = 0
    for col in colunas:
        if df[col].dtype == object:
            original = df[col].copy()
            df[col] = df[col].astype(str).str.strip()
            total_espacos += (original != df[col]).sum()
    return df, total_espacos

def remover_duplicatas(df: pd.DataFrame, coluna: str):
    """
    Remove duplicate rows based on the first column.
    
    Args:
        df (pd.DataFrame): DataFrame to process.
        coluna (str): Column name to check for duplicates.
    
    Returns:
        pd.DataFrame: DataFrame without duplicates.
        int: Number of duplicates removed.
    """
    total_duplicatas = df.duplicated(subset=[coluna]).sum()
    df = df.drop_duplicates(subset=[coluna])
    return df, total_duplicatas

def filtrar_primeira_coluna_por_tamanho(df: pd.DataFrame, coluna: str, min_len: int = 1):
    """
    Remove rows where the first column has fewer than min_len characters.
    
    Args:
        df (pd.DataFrame): DataFrame to filter.
        coluna (str): Column name to check length.
        min_len (int): Minimum number of characters required.
    
    Returns:
        pd.DataFrame: Filtered DataFrame.
        int: Number of rows removed.
    """
    mask = df[coluna].astype(str).str.len() >= min_len
    linhas_removidas = (~mask).sum()
    df = df[mask].copy()
    return df, linhas_removidas
