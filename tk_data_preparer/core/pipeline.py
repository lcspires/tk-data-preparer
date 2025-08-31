from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import pandas as pd

from .cleaning import CleanConfig, clean_columns
from .filtering import FilterConfig, filter_by_length
from .deduplication import DedupConfig, remove_duplicates


@dataclass
class PipelineConfig:
    """
    Configuração para orquestração completa do pipeline de preparação de dados.
    """
    cleaning: Optional[CleanConfig] = None
    filtering: Optional[FilterConfig] = None
    deduplication: Optional[DedupConfig] = None


@dataclass
class PipelineResult:
    dataframe: pd.DataFrame
    metrics: Dict[str, Any] = field(default_factory=dict)


class DataPreparationPipeline:
    """
    Orquestra o fluxo completo de preparação de dados:
    1. Limpeza de colunas
    2. Filtragem por tamanho mínimo
    3. Remoção de duplicatas

    Cada etapa é opcional, dependendo da configuração.
    """

    def __init__(self, config: PipelineConfig):
        self.config = config

    def run(self, df: pd.DataFrame, target_column: str, columns_to_clean: Optional[list[str]] = None) -> PipelineResult:
        metrics: Dict[str, Any] = {}
        current_df = df.copy()

        # 1. Cleaning
        if self.config.cleaning:
            current_df, clean_metrics = clean_columns(
                current_df, columns=columns_to_clean, config=self.config.cleaning
            )
            metrics["cleaning"] = clean_metrics

        # 2. Filtering
        if self.config.filtering:
            current_df, filter_metrics = filter_by_length(
                current_df,
                column=target_column,
                config=self.config.filtering,
            )
            metrics["filtering"] = filter_metrics

        # 3. Deduplication
        if self.config.deduplication:
            current_df, dedup_metrics = remove_duplicates(
                current_df,
                column=target_column,
                config=self.config.deduplication,
            )
            metrics["deduplication"] = dedup_metrics

        return PipelineResult(dataframe=current_df, metrics=metrics)
