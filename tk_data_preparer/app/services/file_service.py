"""
File service for reading and writing various data formats.
"""

import pandas as pd
from typing import Optional, Tuple, Dict, Any  # ✅ Adicionado Dict e Any
from pathlib import Path
import chardet  # ✅ Adicionado chardet


class FileService:
    """Service for file operations with basic encoding detection."""
    
    def load_file(self, filepath: str) -> Tuple[pd.DataFrame, str]:
        """Load file with automatic format detection."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
            
        ext = path.suffix.lower()
        
        try:
            if ext in ['.xls', '.xlsx']:
                df = pd.read_excel(filepath)
                return df, 'excel'
                
            elif ext in ['.csv', '.txt']:
                return self._load_text_file(filepath), 'text'
                
            else:
                raise ValueError(f"Unsupported file type: {ext}")
                
        except Exception as e:
            raise Exception(f"Failed to load file {path.name}: {str(e)}")
            
    def _load_text_file(self, filepath: str) -> pd.DataFrame:
        """Load CSV/TXT file with automatic delimiter detection."""
        # Tenta encodings comuns
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        
        # Tenta delimitadores comuns
        delimiters = [';', ',', '\t', '|']
        
        for encoding in encodings:
            for delimiter in delimiters:
                try:
                    return pd.read_csv(
                        filepath, 
                        delimiter=delimiter, 
                        encoding=encoding,
                        on_bad_lines='skip',
                        quotechar='"',
                        engine='python'
                    )
                except:
                    continue
                    
        # Se nenhum combination funcionar, tenta sem delimiter específico
        for encoding in encodings:
            try:
                return pd.read_csv(
                    filepath,
                    encoding=encoding,
                    on_bad_lines='skip',
                    engine='python'
                )
            except:
                continue
                
        raise ValueError("Cannot read file with any standard encoding or delimiter")
    
    def export_data(self, df: pd.DataFrame, filepath: str, delimiter: str = ';') -> bool:
        """Export data to file with specified format."""
        try:
            path = Path(filepath)
            ext = path.suffix.lower()
            
            if ext == '.xlsx':
                df.to_excel(filepath, index=False)
            else:
                # Para CSV/TXT, usa o delimiter especificado
                df.to_csv(filepath, sep=delimiter, index=False, encoding='utf-8-sig')
                
            return True
            
        except Exception as e:
            raise Exception(f"Failed to export file: {str(e)}")
    
    def detect_file_info(self, filepath: str) -> Dict[str, Any]:
        """Detect file information before loading."""
        path = Path(filepath)
        info = {
            'filename': path.name,
            'extension': path.suffix.lower(),
            'size': path.stat().st_size,
            'size_mb': round(path.stat().st_size / (1024 * 1024), 2)
        }
        
        if info['extension'] in ['.csv', '.txt']:
            try:
                with open(filepath, 'rb') as f:
                    raw_data = f.read(1024)
                    encoding_result = chardet.detect(raw_data)
                    info['encoding'] = encoding_result['encoding'] or 'unknown'
                    info['confidence'] = encoding_result['confidence']
            except:
                info['encoding'] = 'unknown'
                info['confidence'] = 0
                
        return info