"""
Metrics display panel for showing pipeline execution statistics.
Provides visual feedback on data cleaning, filtering, and deduplication results.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Callable  # ✅ ADICIONAR Callable e Optional
import pandas as pd


class MetricsDisplay(ttk.LabelFrame):
    """Panel for displaying pipeline execution metrics."""
    
    def __init__(self, parent, on_metric_click: Optional[Callable] = None):
        super().__init__(parent, text="📈 Processing Metrics", padding=10)
        self.on_metric_click = on_metric_click
        self.metrics: Dict[str, Any] = {}
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup metrics display UI with expandable sections."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='x', expand=True)
        
        # Create tabs for each metric category
        self.summary_tab = ttk.Frame(self.notebook, padding=5)
        self.cleaning_tab = ttk.Frame(self.notebook, padding=5)
        self.filtering_tab = ttk.Frame(self.notebook, padding=5)
        self.deduplication_tab = ttk.Frame(self.notebook, padding=5)
        
        self.notebook.add(self.summary_tab, text="📊 Summary")
        self.notebook.add(self.cleaning_tab, text="🧹 Cleaning")
        self.notebook.add(self.filtering_tab, text="🔍 Filtering")
        self.notebook.add(self.deduplication_tab, text="🚫 Deduplication")
        
        self._setup_summary_tab()
        self._setup_cleaning_tab()
        self._setup_filtering_tab()
        self._setup_deduplication_tab()
        
    def _setup_summary_tab(self):
        """Setup summary metrics tab."""
        # Summary stats frame
        summary_frame = ttk.Frame(self.summary_tab)
        summary_frame.pack(fill='x', pady=5)
        
        # Grid for summary metrics
        ttk.Label(summary_frame, text="Total Rows Processed:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.total_rows_label = ttk.Label(summary_frame, text="0", font=('Arial', 9))
        self.total_rows_label.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(summary_frame, text="Final Rows:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.final_rows_label = ttk.Label(summary_frame, text="0", font=('Arial', 9))
        self.final_rows_label.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(summary_frame, text="Rows Removed:", font=('Arial', 9, 'bold')).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.removed_rows_label = ttk.Label(summary_frame, text="0", font=('Arial', 9))
        self.removed_rows_label.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(summary_frame, text="Reduction:", font=('Arial', 9, 'bold')).grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.reduction_label = ttk.Label(summary_frame, text="0%", font=('Arial', 9))
        self.reduction_label.grid(row=3, column=1, sticky='w', padx=5, pady=2)
        
        # Efficiency metrics
        ttk.Separator(summary_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=10, padx=5)
        
        ttk.Label(summary_frame, text="Processing Time:", font=('Arial', 9, 'bold')).grid(row=5, column=0, sticky='w', padx=5, pady=2)
        self.time_label = ttk.Label(summary_frame, text="N/A", font=('Arial', 9))
        self.time_label.grid(row=5, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(summary_frame, text="Cells Modified:", font=('Arial', 9, 'bold')).grid(row=6, column=0, sticky='w', padx=5, pady=2)
        self.cells_modified_label = ttk.Label(summary_frame, text="0", font=('Arial', 9))
        self.cells_modified_label.grid(row=6, column=1, sticky='w', padx=5, pady=2)
        
    def _setup_cleaning_tab(self):
        """Setup cleaning metrics tab."""
        cleaning_frame = ttk.Frame(self.cleaning_tab)
        cleaning_frame.pack(fill='both', expand=True)
        
        # Whitespace metrics
        ttk.Label(cleaning_frame, text="Whitespace Removal:", font=('Arial', 9, 'bold')).pack(anchor='w', pady=(0, 5))
        
        ttk.Label(cleaning_frame, text="Total Whitespace Characters Removed:").pack(anchor='w', padx=20, pady=1)
        self.ws_total_label = ttk.Label(cleaning_frame, text="0")
        self.ws_total_label.pack(anchor='w', padx=40, pady=1)
        
        # Per-column whitespace
        ttk.Label(cleaning_frame, text="Per Column Removal:", font=('Arial', 9, 'bold')).pack(anchor='w', pady=(10, 5))
        
        self.ws_per_column_frame = ttk.Frame(cleaning_frame)
        self.ws_per_column_frame.pack(fill='x', padx=20, pady=5)
        
        # Other cleaning metrics
        ttk.Label(cleaning_frame, text="Other Metrics:", font=('Arial', 9, 'bold')).pack(anchor='w', pady=(10, 5))
        
        ttk.Label(cleaning_frame, text="Empty Strings Converted to NA:").pack(anchor='w', padx=20, pady=1)
        self.empty_to_na_label = ttk.Label(cleaning_frame, text="0")
        self.empty_to_na_label.pack(anchor='w', padx=40, pady=1)
        
        ttk.Label(cleaning_frame, text="Total Cells Modified:").pack(anchor='w', padx=20, pady=1)
        self.cleaning_cells_label = ttk.Label(cleaning_frame, text="0")
        self.cleaning_cells_label.pack(anchor='w', padx=40, pady=1)
        
    def _setup_filtering_tab(self):
        """Setup filtering metrics tab."""
        filtering_frame = ttk.Frame(self.filtering_tab)
        filtering_frame.pack(fill='both', expand=True)
        
        ttk.Label(filtering_frame, text="Filtering Results:", font=('Arial', 9, 'bold')).pack(anchor='w', pady=(0, 5))
        
        ttk.Label(filtering_frame, text="Rows Removed by Filtering:").pack(anchor='w', padx=20, pady=1)
        self.filtered_rows_label = ttk.Label(filtering_frame, text="0")
        self.filtered_rows_label.pack(anchor='w', padx=40, pady=1)
        
        ttk.Label(filtering_frame, text="Minimum Length Requirement:").pack(anchor='w', padx=20, pady=1)
        self.min_length_label = ttk.Label(filtering_frame, text="N/A")
        self.min_length_label.pack(anchor='w', padx=40, pady=1)
        
        ttk.Label(filtering_frame, text="NA Rows Handling:").pack(anchor='w', padx=20, pady=1)
        self.na_handling_label = ttk.Label(filtering_frame, text="N/A")
        self.na_handling_label.pack(anchor='w', padx=40, pady=1)
        
        ttk.Label(filtering_frame, text="Remaining Rows After Filtering:").pack(anchor='w', padx=20, pady=1)
        self.remaining_filtered_label = ttk.Label(filtering_frame, text="0")
        self.remaining_filtered_label.pack(anchor='w', padx=40, pady=1)
        
    def _setup_deduplication_tab(self):
        """Setup deduplication metrics tab."""
        dedup_frame = ttk.Frame(self.deduplication_tab)
        dedup_frame.pack(fill='both', expand=True)
        
        ttk.Label(dedup_frame, text="Deduplication Results:", font=('Arial', 9, 'bold')).pack(anchor='w', pady=(0, 5))
        
        ttk.Label(dedup_frame, text="Duplicate Rows Removed:").pack(anchor='w', padx=20, pady=1)
        self.duplicates_removed_label = ttk.Label(dedup_frame, text="0")
        self.duplicates_removed_label.pack(anchor='w', padx=40, pady=1)
        
        ttk.Label(dedup_frame, text="Keep Strategy:").pack(anchor='w', padx=20, pady=1)
        self.keep_strategy_label = ttk.Label(dedup_frame, text="N/A")
        self.keep_strategy_label.pack(anchor='w', padx=40, pady=1)
        
        ttk.Label(dedup_frame, text="Case Sensitivity:").pack(anchor='w', padx=20, pady=1)
        self.case_sensitive_label = ttk.Label(dedup_frame, text="N/A")
        self.case_sensitive_label.pack(anchor='w', padx=40, pady=1)
        
        ttk.Label(dedup_frame, text="Unicode Normalization:").pack(anchor='w', padx=20, pady=1)
        self.unicode_norm_label = ttk.Label(dedup_frame, text="N/A")
        self.unicode_norm_label.pack(anchor='w', padx=40, pady=1)
        
        ttk.Label(dedup_frame, text="Remaining Unique Rows:").pack(anchor='w', padx=20, pady=1)
        self.remaining_unique_label = ttk.Label(dedup_frame, text="0")
        self.remaining_unique_label.pack(anchor='w', padx=40, pady=1)
        
    def update_metrics(self, metrics: Dict[str, Any]):
        """Update metrics display with new data."""
        self.metrics = metrics
        self._update_summary_tab()
        self._update_cleaning_tab()
        self._update_filtering_tab()
        self._update_deduplication_tab()
        
    def _update_summary_tab(self):
        """Update summary tab with metrics."""
        # Calculate summary statistics
        initial_rows = self.metrics.get('initial_rows', 0)
        final_rows = self.metrics.get('final_rows', 0)
        removed_rows = initial_rows - final_rows if initial_rows and final_rows else 0
        
        reduction_pct = (removed_rows / initial_rows * 100) if initial_rows > 0 else 0
        
        self.total_rows_label.config(text=f"{initial_rows:,}")
        self.final_rows_label.config(text=f"{final_rows:,}")
        self.removed_rows_label.config(text=f"{removed_rows:,}")
        self.reduction_label.config(text=f"{reduction_pct:.1f}%")
        
        # Additional metrics
        cells_modified = self.metrics.get('cleaning', {}).get('cells_modified', 0)
        self.cells_modified_label.config(text=f"{cells_modified:,}")
        
    def _update_cleaning_tab(self):
        """Update cleaning tab with metrics."""
        cleaning_metrics = self.metrics.get('cleaning', {})
        
        # Whitespace metrics
        ws_total = cleaning_metrics.get('total_whitespace_removed', 0)
        self.ws_total_label.config(text=f"{ws_total:,}")
        
        # Per-column whitespace
        for widget in self.ws_per_column_frame.winfo_children():
            widget.destroy()
            
        per_column = cleaning_metrics.get('per_column_whitespace_removed', {})
        if per_column:
            row = 0
            for col, count in per_column.items():
                ttk.Label(self.ws_per_column_frame, text=f"{col}:").grid(row=row, column=0, sticky='w', padx=(0, 5))
                ttk.Label(self.ws_per_column_frame, text=f"{count:,}").grid(row=row, column=1, sticky='w')
                row += 1
        else:
            ttk.Label(self.ws_per_column_frame, text="No whitespace removed").grid(row=0, column=0, sticky='w')
        
        # Other cleaning metrics
        empty_to_na = cleaning_metrics.get('empty_strings_to_na', 0)
        cells_modified = cleaning_metrics.get('cells_modified', 0)
        
        self.empty_to_na_label.config(text=f"{empty_to_na:,}")
        self.cleaning_cells_label.config(text=f"{cells_modified:,}")
        
    def _update_filtering_tab(self):
        """Update filtering tab with metrics."""
        filtering_metrics = self.metrics.get('filtering', {})
        
        removed = filtering_metrics.get('removed_rows', 0)
        remaining = filtering_metrics.get('remaining_rows', 0)
        min_length = filtering_metrics.get('min_length', 'N/A')
        drop_na = filtering_metrics.get('drop_na', False)
        
        self.filtered_rows_label.config(text=f"{removed:,}")
        self.min_length_label.config(text=f"{min_length} characters")
        self.na_handling_label.config(text="Removed" if drop_na else "Kept")
        self.remaining_filtered_label.config(text=f"{remaining:,}")
        
    def _update_deduplication_tab(self):
        """Update deduplication tab with metrics."""
        dedup_metrics = self.metrics.get('deduplication', {})
        
        removed = dedup_metrics.get('removed_duplicates', 0)
        remaining = dedup_metrics.get('remaining_rows', 0)
        keep_strategy = dedup_metrics.get('keep_strategy', 'N/A')
        case_sensitive = dedup_metrics.get('case_sensitive', False)
        unicode_norm = dedup_metrics.get('normalize_unicode', False)
        
        self.duplicates_removed_label.config(text=f"{removed:,}")
        self.keep_strategy_label.config(text=keep_strategy)
        self.case_sensitive_label.config(text="Yes" if case_sensitive else "No")
        self.unicode_norm_label.config(text="Yes" if unicode_norm else "No")
        self.remaining_unique_label.config(text=f"{remaining:,}")
        
    def clear(self):
        """Clear all metrics display."""
        self.metrics = {}
        
        # Clear all labels
        for tab in [self.summary_tab, self.cleaning_tab, self.filtering_tab, self.deduplication_tab]:
            for widget in tab.winfo_children():
                if isinstance(widget, ttk.Label) and not isinstance(widget, ttk.LabelFrame):
                    widget.config(text="0")
        
        # Clear per-column frame
        for widget in self.ws_per_column_frame.winfo_children():
            widget.destroy()
            
        # Reset specific labels
        self.total_rows_label.config(text="0")
        self.final_rows_label.config(text="0")
        self.removed_rows_label.config(text="0")
        self.reduction_label.config(text="0%")
        self.min_length_label.config(text="N/A")
        self.na_handling_label.config(text="N/A")
        self.keep_strategy_label.config(text="N/A")
        self.case_sensitive_label.config(text="N/A")
        self.unicode_norm_label.config(text="N/A")