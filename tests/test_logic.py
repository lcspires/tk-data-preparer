import pytest
import pandas as pd
from tk_data_preparer.logic import (
    limpar_espacos_em_colunas,
    remover_duplicatas,
    filtrar_primeira_coluna_por_tamanho,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Name": ["Lucas", "Raquel", "Gabriel", "Beatriz", "Levi"],
        "Code": ["123", "45", "6789", "45", "12"],
        "Value": [100, 200, 300, 200, 400],
    })


def test_limpar_espacos_em_colunas(sample_df):
    df_dirty = sample_df.copy()
    df_dirty.loc[1, "Name"] = " Raquel "
    df_dirty.loc[2, "Name"] = " Gabriel"
    df_clean, total_espacos = limpar_espacos_em_colunas(df_dirty)
    assert df_clean["Name"].iloc[1] == "Raquel"
    assert df_clean["Name"].iloc[2] == "Gabriel"
    assert total_espacos == 3  # três espaços removidos no total


def test_remover_duplicatas(sample_df):
    df_dup = sample_df.copy()
    df_dup.loc[5] = ["Lucas", "123", 100]  # adicionar duplicata
    df_unique, removidas = remover_duplicatas(df_dup, "Code")
    assert df_unique.shape[0] == df_dup.shape[0] - removidas
    assert removidas == 2  # "123" e "45" duplicadas removidas


def test_filtrar_primeira_coluna_por_tamanho(sample_df):
    df_filtrado, removidas = filtrar_primeira_coluna_por_tamanho(
        sample_df.copy(), "Code", min_len=3
    )
    # "45" aparece duas vezes e "12" uma vez → total 3 linhas removidas
    assert removidas == 3
    assert df_filtrado.shape[0] == 2
    assert all(df_filtrado["Code"].str.len() >= 3)
