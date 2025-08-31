"""
Pipeline service for executing data processing operations.
"""

import time
from typing import Dict, Any
import pandas as pd

from tk_data_preparer.core import DataPreparationPipeline, PipelineResult, PipelineConfig


class PipelineService:
    """Service for executing data processing pipeline."""
    
    def __init__(self):
        self.pipeline = DataPreparationPipeline(PipelineConfig())
        
    def execute_pipeline(self, data: pd.DataFrame, config: PipelineConfig) -> PipelineResult:
        """Execute pipeline with timing and enhanced metrics."""
        start_time = time.time()
        
        # Store initial row count for summary metrics
        initial_rows = len(data)
        
        # Execute pipeline
        result = self.pipeline.run(
            data, 
            target_column=data.columns[0] if not data.empty else '',  # Use first column as target
            columns_to_clean=data.columns.tolist()
        )
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Enhance metrics with additional information
        enhanced_metrics = self._enhance_metrics(result.metrics, initial_rows, execution_time)
        result.metrics = enhanced_metrics
        
        return result
        
    def _enhance_metrics(self, metrics: Dict[str, Any], initial_rows: int, execution_time: float) -> Dict[str, Any]:
        """Enhance metrics with additional calculated values."""
        # Get final row count from the last step that has remaining_rows
        final_rows = initial_rows
        for step_metrics in metrics.values():
            if 'remaining_rows' in step_metrics:
                final_rows = step_metrics['remaining_rows']
        
        enhanced = metrics.copy()
        enhanced['initial_rows'] = initial_rows
        enhanced['final_rows'] = final_rows
        enhanced['execution_time'] = round(execution_time, 3)
        enhanced['total_removed'] = initial_rows - final_rows
        
        # Calculate reduction percentage
        if initial_rows > 0:
            enhanced['reduction_percentage'] = round((enhanced['total_removed'] / initial_rows) * 100, 1)
        else:
            enhanced['reduction_percentage'] = 0.0
            
        return enhanced