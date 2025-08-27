import pandas as pd


def limpar_espacos_em_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove espaços extras (strip) em todas as colunas de string.
    """
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def remover_duplicatas(df: pd.DataFrame, coluna: str = None) -> pd.DataFrame:
    """
    Remove linhas duplicadas.
    Se 'coluna' for especificada, usa apenas essa coluna para considerar duplicação.
    """
    if coluna and coluna in df.columns:
        return df.drop_duplicates(subset=[coluna])
    return df.drop_duplicates()


def filtrar_primeira_coluna_por_tamanho(
    df: pd.DataFrame, coluna: str, min_len: int = 3
) -> tuple[pd.DataFrame, int]:
    """
    Remove linhas cuja string na coluna especificada tenha tamanho menor que min_len.
    Retorna o DataFrame filtrado e a quantidade de linhas removidas.
    """
    if coluna not in df.columns:
        raise ValueError(f"A coluna '{coluna}' não existe no DataFrame.")

    tamanho_inicial = df.shape[0]
    df_filtrado = df[df[coluna].astype(str).str.len() >= min_len]
    linhas_removidas = tamanho_inicial - df_filtrado.shape[0]

    return df_filtrado, linhas_removidas
