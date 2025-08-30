import pytest
import pandas as pd
from tk_data_preparer.logic import (
    limpar_espacos_em_colunas,
    filtrar_primeira_coluna_por_tamanho,
    remover_duplicatas
)


@pytest.fixture
def sample_df():
    """Returns a small sample DataFrame for testing."""
    data = {
        "Name": [" Alice  ", "Bob", "Charlie ", "Bob", "Eve"],
        "Code": ["123", "45", "6789", "45", "12"],
        "Value": [" 100 ", "200", " 300", "200", " 400 "]
    }
    return pd.DataFrame(data)


def test_limpar_espacos_em_colunas(sample_df):
    df_cleaned, total_spaces = limpar_espacos_em_colunas(sample_df.copy(), ["Name", "Value"])
    assert df_cleaned["Name"].tolist() == ["Alice", "Bob", "Charlie", "Bob", "Eve"]
    assert df_cleaned["Value"].tolist() == ["100", "200", "300", "200", "400"]
    assert total_spaces > 0


def test_filtrar_primeira_coluna_por_tamanho(sample_df):
    # Filter rows where 'Code' has at least 3 characters
    df_filtered, rows_removed = filtrar_primeira_coluna_por_tamanho(sample_df.copy(), "Code", min_len=3)
    # Only "123" and "6789" pass
    assert df_filtered.shape[0] == 2
    assert all(df_filtered["Code"].astype(str).str.len() >= 3)
    # Rows removed: 5 - 2 = 3
    assert rows_removed == 3


def test_remover_duplicatas(sample_df):
    # Remove duplicates based on 'Name'
    df_no_dupes, dupes_removed = remover_duplicatas(sample_df.copy(), "Name")
    # Unique names: " Alice  ", "Bob", "Charlie ", "Eve"
    assert df_no_dupes.shape[0] == 4
    assert dupes_removed == 1
    assert df_no_dupes["Name"].tolist() == [" Alice  ", "Bob", "Charlie ", "Eve"]
