import pytest
import pandas as pd
from tk_data_preparer.logic import (
    limpar_espacos_em_colunas,
    remover_duplicatas,
    filtrar_primeira_coluna_por_tamanho,
)


@pytest.fixture
def sample_df():
    data = {
        "Name": ["Lucas", "Raquel", "Gabriel", "Beatriz", "Levi"],
        "Code": ["123", "45", "6789", "45", "12"],
        "Value": [100, 200, 300, 200, 400],
    }
    return pd.DataFrame(data)


def test_limpar_espacos_em_colunas(sample_df):
    # adicionando espaços artificiais para validar
    sample_df["Name"] = [" Lucas ", " Raquel ", " Gabriel ", " Beatriz ", " Levi "]
    df_clean = limpar_espacos_em_colunas(sample_df.copy())
    assert all(df_clean["Name"].str.strip() == df_clean["Name"])


def test_remover_duplicatas(sample_df):
    df_unique = remover_duplicatas(sample_df.copy(), "Code")
    # deve remover uma das linhas "45"
    assert df_unique.shape[0] == 4
    assert df_unique["Code"].duplicated().sum() == 0


def test_filtrar_primeira_coluna_por_tamanho(sample_df):
    df_filtered, rows_removed = filtrar_primeira_coluna_por_tamanho(
        sample_df.copy(), "Code", min_len=3
    )
    # Apenas "123" (len=3) e "6789" (len=4) permanecem
    assert df_filtered.shape[0] == 2
    assert all(df_filtered["Code"].str.len() >= 3)
    assert rows_removed == 3
