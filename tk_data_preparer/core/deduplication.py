from dataclasses import dataclass
from typing import Literal, Dict, Any
import pandas as pd


@dataclass
class DedupConfig:
    """
    Configurações para operações de remoção de duplicatas.
    """
    keep: Literal["first", "last", False] = "first"  # estratégia do pandas.drop_duplicates
    case_sensitive: bool = True                      # diferenciação de maiúsculas/minúsculas
    normalize_unicode: bool = False                  # normaliza strings antes de deduplicar (NFKC)


def remove_duplicates(
    df: pd.DataFrame,
    column: str,
    config: DedupConfig
) -> tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Remove duplicatas de um DataFrame baseado na coluna especificada.
    - Retorna um novo DataFrame.
    - Métricas incluem número de duplicatas removidas e registros únicos.
    """
    import unicodedata

    tamanho_anterior = len(df)
    series = df[column].astype(str)

    if not config.case_sensitive:
        series = series.str.lower()
    if config.normalize_unicode:
        series = series.map(lambda x: unicodedata.normalize("NFKC", x))

    # cria cópia com coluna auxiliar
    df_aux = df.copy()
    df_aux["__dedup_key__"] = series

    df_filtrado = df_aux.drop_duplicates(
        subset=["__dedup_key__"], keep=config.keep
    ).drop(columns=["__dedup_key__"])

    duplicatas_removidas = tamanho_anterior - len(df_filtrado)

    metrics = {
        "removed_duplicates": duplicatas_removidas,
        "remaining_rows": len(df_filtrado),
        "keep_strategy": config.keep,
        "case_sensitive": config.case_sensitive,
        "normalize_unicode": config.normalize_unicode,
    }
    return df_filtrado, metrics
