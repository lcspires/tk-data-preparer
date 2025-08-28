import pandas as pd


def limpar_espacos_em_colunas(df: pd.DataFrame):
    """
    Remove espaços em branco extras de todas as colunas do DataFrame.
    Retorna o DataFrame limpo e o total de espaços removidos.
    """
    total_removidos = 0
    for col in df.columns:
        if df[col].dtype == object:
            antes = df[col].astype(str).str.len().sum()
            df[col] = df[col].astype(str).str.strip()
            depois = df[col].astype(str).str.len().sum()
            total_removidos += int(antes - depois)
    return df, total_removidos


def remover_duplicatas(df: pd.DataFrame, coluna: str):
    """
    Remove linhas duplicadas com base em uma coluna específica.
    Retorna o DataFrame sem duplicatas e o número de linhas removidas.
    """
    antes = len(df)
    df = df.drop_duplicates(subset=[coluna], keep="first")
    depois = len(df)
    removidas = antes - depois
    return df, removidas


def filtrar_primeira_coluna_por_tamanho(df: pd.DataFrame, coluna: str, min_len: int = 3):
    """
    Filtra linhas onde o valor da primeira coluna tem pelo menos `min_len` caracteres.
    Retorna o DataFrame filtrado e o número de linhas removidas.
    """
    antes = len(df)
    df = df[df[coluna].astype(str).str.len() >= min_len]
    depois = len(df)
    removidas = antes - depois
    return df, removidas
