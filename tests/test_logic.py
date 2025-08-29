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
    assert total_espacos == 3  # 2 espaços em " Raquel " + 1 em " Gabriel"


def test_remover_duplicatas(sample_df):
    df_dup = sample_df.copy()
    df_dup.loc[5] = ["Lucas", "123", 100]  # adicionar duplicata
    df_unique, removidas = remover_duplicatas(df_dup, "Code")
    assert df_unique.shape[0] == df_dup.shape[0] - removidas
    assert removidas == 2  # "123" e "45" duplicadas removidas


@pytest.mark.parametrize("min_len,expected_removed,expected_remaining", [
    (3, 3, 2),  # remove "45"(2x) + "12"(1x)
    (4, 4, 1),  # remove tudo menos "6789"
    (1, 0, 5),  # ninguém removido
])
def test_filtrar_primeira_coluna_por_tamanho(sample_df, min_len, expected_removed, expected_remaining):
    df_filtrado, removidas = filtrar_primeira_coluna_por_tamanho(
        sample_df.copy(), "Code", min_len=min_len
    )
    assert removidas == expected_removed
    assert df_filtrado.shape[0] == expected_remaining
    assert all(df_filtrado["Code"].str.len() >= min_len)
