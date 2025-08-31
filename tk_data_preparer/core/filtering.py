from dataclasses import dataclass
from typing import Optional, Dict, Any
import pandas as pd


@dataclass
class FilterConfig:
    """
    Configurações para operações de filtragem.
    """
    min_length: Optional[int] = None  # comprimento mínimo para a primeira coluna
    drop_na: bool = False             # se deve remover linhas com NA na primeira coluna


def filter_by_length(
    df: pd.DataFrame,
    column: str,
    config: FilterConfig
) -> tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Remove linhas cuja string na coluna especificada não atinge o comprimento mínimo.
    Retorna um novo DataFrame e métricas da filtragem.
    """
    if config.min_length is None:
        return df.copy(), {"removed_rows": 0, "reason": "no min_length set"}

    tamanho_anterior = len(df)
    mask = df[column].astype(str).str.len() >= config.min_length

    # manter NaN se drop_na for False
    if not config.drop_na:
        mask |= df[column].isna()

    df_filtrado = df[mask].copy()
    linhas_removidas = tamanho_anterior - len(df_filtrado)

    metrics = {
        "removed_rows": linhas_removidas,
        "remaining_rows": len(df_filtrado),
        "min_length": config.min_length,
        "drop_na": config.drop_na,
    }
    return df_filtrado, metrics


def drop_na_rows(
    df: pd.DataFrame,
    column: str
) -> tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Remove linhas com NA/NaN na coluna especificada.
    """
    tamanho_anterior = len(df)
    df_filtrado = df.dropna(subset=[column]).copy()
    linhas_removidas = tamanho_anterior - len(df_filtrado)

    metrics = {
        "removed_rows": linhas_removidas,
        "remaining_rows": len(df_filtrado),
        "drop_na_column": column,
    }
    return df_filtrado, metrics
