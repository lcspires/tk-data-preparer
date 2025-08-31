"""
Application state management using observer pattern.
Centralized state management for the entire application.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import pandas as pd

from tk_data_preparer.core import AppConfig, PipelineResult


@dataclass
class AppState:
    """Centralized application state management with observer pattern."""
    
    current_data: Optional[pd.DataFrame] = None
    current_columns: List[str] = field(default_factory=list)
    current_config: AppConfig = field(default_factory=AppConfig.get_default)
    pipeline_result: Optional[PipelineResult] = None
    current_filepath: Optional[str] = None
    _observers: Dict[str, List[Callable]] = field(default_factory=dict)
    
    @property
    def has_data(self) -> bool:
        """Check if there is loaded data."""
        return self.current_data is not None and not self.current_data.empty
    
    @property
    def has_processed_data(self) -> bool:
        """Check if there is processed data from pipeline."""
        return self.pipeline_result is not None and self.pipeline_result.dataframe is not None
    
    @property
    def has_selected_columns(self) -> bool:
        """Check if columns are selected."""
        return len(self.current_columns) > 0
    
    @property
    def initial_rows_count(self) -> int:
        """Get initial number of rows in loaded data."""
        return len(self.current_data) if self.has_data else 0
    
    @property
    def processed_rows_count(self) -> int:
        """Get number of rows after processing."""
        if self.has_processed_data:
            return len(self.pipeline_result.dataframe)
        return self.initial_rows_count
    
    def set_data(self, data: pd.DataFrame, filepath: Optional[str] = None):
        """Set new data and notify observers."""
        self.current_data = data
        self.current_filepath = filepath
        self.pipeline_result = None  # Reset pipeline result when new data is loaded
        self._notify('data_loaded', data)
        
    def set_config(self, config: AppConfig):
        """Set new configuration and notify observers."""
        self.current_config = config
        self._notify('config_changed', config)
        
    def set_columns(self, columns: List[str]):
        """Set current column selection and notify observers."""
        self.current_columns = columns
        self._notify('columns_changed', columns)
        
    def set_pipeline_result(self, result: PipelineResult):
        """Set pipeline result and notify observers."""
        self.pipeline_result = result
        self._notify('pipeline_executed', result)
        
    def subscribe(self, event: str, callback: Callable):
        """Subscribe to state changes."""
        if event not in self._observers:
            self._observers[event] = []
        self._observers[event].append(callback)
        
    def unsubscribe(self, event: str, callback: Callable):
        """Unsubscribe from state changes."""
        if event in self._observers:
            if callback in self._observers[event]:
                self._observers[event].remove(callback)
                
    def get_processed_metrics(self) -> Optional[Dict[str, Any]]:
        """Get processed metrics if available."""
        if self.has_processed_data and self.pipeline_result.metrics:
            return self.pipeline_result.metrics
        return None
        
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get summary of processing results."""
        summary = {
            'initial_rows': self.initial_rows_count,
            'processed_rows': self.processed_rows_count,
            'rows_removed': self.initial_rows_count - self.processed_rows_count,
            'reduction_percentage': 0.0,
            'has_processed_data': self.has_processed_data
        }
        
        if summary['initial_rows'] > 0:
            summary['reduction_percentage'] = (
                (summary['rows_removed'] / summary['initial_rows']) * 100
            )
            
        return summary
        
    def reset(self):
        """Reset all state to initial values."""
        previous_data = self.current_data
        previous_config = self.current_config
        
        self.current_data = None
        self.current_columns = []
        self.current_config = AppConfig.get_default()
        self.pipeline_result = None
        self.current_filepath = None
        
        # Notify observers of reset
        self._notify('reset', {
            'previous_data': previous_data,
            'previous_config': previous_config
        })
        
    def _notify(self, event: str, data: Any = None):
        """Notify all observers of an event."""
        for callback in self._observers.get(event, []):
            try:
                callback(data)
            except Exception as e:
                print(f"Error in observer callback for event {event}: {e}")
                
    def get_state_info(self) -> Dict[str, Any]:
        """Get comprehensive state information for debugging."""
        return {
            'has_data': self.has_data,
            'has_processed_data': self.has_processed_data,
            'has_selected_columns': self.has_selected_columns,
            'data_shape': self.current_data.shape if self.has_data else None,
            'columns_count': len(self.current_columns),
            'config': self.current_config.to_dict() if self.current_config else None,
            'filepath': self.current_filepath,
            'pipeline_has_result': self.pipeline_result is not None,
            'observers_count': {k: len(v) for k, v in self._observers.items()}
        }


# Singleton instance for easy access (optional)
_app_state_instance: Optional[AppState] = None

def get_app_state() -> AppState:
    """Get singleton application state instance."""
    global _app_state_instance
    if _app_state_instance is None:
        _app_state_instance = AppState()
    return _app_state_instance


def reset_app_state():
    """Reset the singleton application state."""
    global _app_state_instance
    _app_state_instance = AppState()