"""
Sistema de configuração para o pipeline de preparação de dados.

Fornece configurações padrão, validação e carregamento de presets.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import json
from pathlib import Path

from .cleaning import CleanConfig
from .filtering import FilterConfig
from .deduplication import DedupConfig
from .pipeline import PipelineConfig


@dataclass
class AppConfig:
    """Configuração completa da aplicação."""
    
    # Configurações do pipeline
    pipeline: PipelineConfig
    
    # Configurações de UI/UX
    default_input_encoding: str = 'utf-8'
    default_delimiter: str = ','
    auto_detect_file_type: bool = True
    max_file_size_mb: int = 50
    
    # Configurações de exportação
    default_export_format: str = 'csv'  # csv, excel, json
    export_include_metrics: bool = True
    
    @classmethod
    def get_default(cls) -> 'AppConfig':
        """Retorna configuração padrão para a aplicação."""
        return cls(
            pipeline=PipelineConfig(
                cleaning=CleanConfig(
                    strip=True,
                    collapse_whitespace=True,
                    unicode_normalization='NFKC',
                    case='lower',
                    empty_to_na=True
                ),
                filtering=FilterConfig(
                    min_length=3,
                    drop_na=True
                ),
                deduplication=DedupConfig(
                    keep='first',
                    case_sensitive=False,
                    normalize_unicode=True
                )
            )
        )
    
    @classmethod
    def get_preset(cls, preset_name: str) -> 'AppConfig':
        """Retorna configuração predefinida baseada no tipo de dados."""
        presets = {
            'customer_data': cls(
                pipeline=PipelineConfig(
                    cleaning=CleanConfig(
                        strip=True,
                        collapse_whitespace=True,
                        case='title',
                        empty_to_na=True
                    ),
                    filtering=FilterConfig(min_length=5, drop_na=True),
                    deduplication=DedupConfig(keep='first', case_sensitive=False)
                )
            ),
            'product_catalog': cls(
                pipeline=PipelineConfig(
                    cleaning=CleanConfig(
                        strip=True,
                        unicode_normalization='NFKC',
                        case='lower'
                    ),
                    filtering=FilterConfig(min_length=2, drop_na=False),
                    deduplication=DedupConfig(keep='first', case_sensitive=True)
                )
            ),
            'minimal': cls(
                pipeline=PipelineConfig(
                    cleaning=CleanConfig(strip=True),
                    filtering=None,
                    deduplication=None
                )
            )
        }
        return presets.get(preset_name, cls.get_default())
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário."""
        return {
            'pipeline': {
                'cleaning': asdict(self.pipeline.cleaning) if self.pipeline.cleaning else None,
                'filtering': asdict(self.pipeline.filtering) if self.pipeline.filtering else None,
                'deduplication': asdict(self.pipeline.deduplication) if self.pipeline.deduplication else None,
            },
            'default_input_encoding': self.default_input_encoding,
            'default_delimiter': self.default_delimiter,
            'auto_detect_file_type': self.auto_detect_file_type,
            'max_file_size_mb': self.max_file_size_mb,
            'default_export_format': self.default_export_format,
            'export_include_metrics': self.export_include_metrics
        }
    
    def save_to_file(self, filepath: Path) -> None:
        """Salva configuração em arquivo JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: Path) -> 'AppConfig':
        """Carrega configuração de arquivo JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        pipeline_data = data.get('pipeline', {})
        return cls(
            pipeline=PipelineConfig(
                cleaning=CleanConfig(**pipeline_data['cleaning']) if pipeline_data.get('cleaning') else None,
                filtering=FilterConfig(**pipeline_data['filtering']) if pipeline_data.get('filtering') else None,
                deduplication=DedupConfig(**pipeline_data['deduplication']) if pipeline_data.get('deduplication') else None,
            ),
            default_input_encoding=data.get('default_input_encoding', 'utf-8'),
            default_delimiter=data.get('default_delimiter', ','),
            auto_detect_file_type=data.get('auto_detect_file_type', True),
            max_file_size_mb=data.get('max_file_size_mb', 50),
            default_export_format=data.get('default_export_format', 'csv'),
            export_include_metrics=data.get('export_include_metrics', True)
        )


# Configurações padrão para acesso fácil
DEFAULT_CONFIG = AppConfig.get_default()
PRESET_CONFIGS = {
    'customer_data': AppConfig.get_preset('customer_data'),
    'product_catalog': AppConfig.get_preset('product_catalog'),
    'minimal': AppConfig.get_preset('minimal')
}