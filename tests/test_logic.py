# tests/test_logic.py - Day 1 MVP (corrigido)

import pandas as pd
import pytest
from tk_data_preparer.logic import (
    limpar_espacos_em_colunas,
    remover_duplicatas,
    filtrar_primeira_coluna_por_tamanho
)

@pytest.fixture
def sample_df():
    data = {
        "Name": ["Alice ", " Bob", "Charlie", "Bob", "Eve "],
        "Code": ["123", "45", "6789", "45", "12"],
        "Value": [100, 200, 300, 200, 400]
    }
    return pd.DataFrame(data)

def test_limpar_espacos_em_colunas(sample_df):
    df_clean, total_removed = limpar_espacos_em_colunas(sample_df.copy(), ["Name"])
    assert df_clean["Name"].iloc[0] == "Alice"
    assert df_clean["Name"].iloc[1] == "Bob"
    assert total_removed == 3  # espaços removidos de 3 células

def test_remover_duplicatas(sample_df):
    df_no_dup, total_dup = remover_duplicatas(sample_df.copy(), "Code")
    assert df_no_dup.shape[0] == 4
    assert total_dup == 1  # "45" duplicado

def test_filtrar_primeira_coluna_por_tamanho(sample_df):
    df_filtered, rows_removed = filtrar_primeira_coluna_por_tamanho(sample_df.copy(), "Code", min_len=3)
    assert df_filtered.shape[0] == 2  # apenas "123" e "6789" permanecem
    assert rows_removed == 3           # linhas removidas: "45", "45", "12"
