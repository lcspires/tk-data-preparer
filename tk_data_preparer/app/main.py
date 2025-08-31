"""
Main application entry point for Tk Data Preparer.
Modern Tkinter application with separated concerns and professional architecture.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Dict, Any
from pathlib import Path
import pandas as pd

from .components.file_loader import FileLoaderPanel
from .components.column_editor import ColumnEditorPanel
from .components.config_panel import ConfigPanel
from .components.preview_panel import PreviewPanel
from .components.metrics_display import MetricsDisplay
from .services.state_service import AppState
from .services.pipeline_service import PipelineService
from .services.file_service import FileService
from .utils.theme import apply_theme, STYLES, COLOR_SCHEME


class TkDataPreparerApp:
    """Main application class with modern architecture."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Tk Data Preparer - Professional Edition")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Application state and services
        self.state = AppState()
        self.pipeline_service = PipelineService()
        self.file_service = FileService()
        
        # Apply modern theme
        apply_theme(self.root)
        
        self._setup_ui()
        self._setup_bindings()
        self._setup_menu()
        
    def _setup_ui(self):
        """Setup modern UI layout with notebook tabs."""
        # Main container with padding
        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Notebook for tabbed interface
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Tab 1: Data Loading and Configuration
        self.tab_data = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_data, text="📁 Data & Configuration")
        
        # Tab 2: Preview and Export
        self.tab_preview = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_preview, text="👀 Preview & Export")
        
        # Initialize components
        self._init_data_tab()
        self._init_preview_tab()
        
        # Status bar
        self.status_bar = ttk.Label(main_container, text="Ready to load data", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Initially disable preview tab until data is loaded
        self.notebook.tab(1, state='disabled')
        
    def _setup_menu(self):
        """Setup application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File", command=self._menu_open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Export Results", command=self._menu_export, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Run Pipeline", command=self._menu_run_pipeline, accelerator="F5")
        edit_menu.add_command(label="Reset All", command=self._menu_reset, accelerator="Ctrl+R")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Data Tab", command=lambda: self.notebook.select(0))
        view_menu.add_command(label="Preview Tab", command=lambda: self.notebook.select(1))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._menu_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self._menu_open_file())
        self.root.bind('<Control-e>', lambda e: self._menu_export())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F5>', lambda e: self._menu_run_pipeline())
        self.root.bind('<Control-r>', lambda e: self._menu_reset())
        
    def _init_data_tab(self):
        """Initialize data loading and configuration tab."""
        # File loader
        self.file_loader = FileLoaderPanel(self.tab_data, self._on_file_loaded)
        self.file_loader.pack(fill=tk.X, pady=(0, 10))
        
        # Configuration panel
        self.config_panel = ConfigPanel(self.tab_data, self._on_config_changed)
        self.config_panel.pack(fill=tk.X, pady=(0, 10))
        
        # Column editor
        self.column_editor = ColumnEditorPanel(self.tab_data, self._on_columns_changed)
        self.column_editor.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
    def _init_preview_tab(self):
        """Initialize preview and export tab."""
        # Preview panel
        self.preview_panel = PreviewPanel(self.tab_preview, self._on_preview_selection)
        self.preview_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Metrics display
        self.metrics_display = MetricsDisplay(self.tab_preview, self._on_metric_click)
        self.metrics_display.pack(fill=tk.X, pady=(0, 10))
        
        # Export button
        export_frame = ttk.Frame(self.tab_preview)
        export_frame.pack(fill=tk.X)
        
        ttk.Button(
            export_frame, 
            text="🚀 Export Processed Data", 
            command=self._export_data,
            style="Accent.TButton",
            state='disabled'
        ).pack(pady=10)
        self.export_button = export_frame.winfo_children()[0]
        
    def _setup_bindings(self):
        """Setup event bindings and observers."""
        # Subscribe to state changes
        self.state.subscribe('data_loaded', self._on_data_loaded)
        self.state.subscribe('config_changed', self._on_config_changed)
        self.state.subscribe('columns_changed', self._on_columns_changed)
        self.state.subscribe('pipeline_executed', self._on_pipeline_executed)
        
    def _on_file_loaded(self, data: pd.DataFrame, filepath: str):
        """Handle file loaded event from file loader."""
        self.state.set_data(data)
        self.column_editor.set_columns(data.columns.tolist())
        self.status_bar.config(text=f"Loaded: {Path(filepath).name} ({len(data)} rows)")
        
        # Enable preview tab
        self.notebook.tab(1, state='normal')
        
    def _on_config_changed(self, config):
        """Handle configuration changed event."""
        self.state.set_config(config)
        
    def _on_columns_changed(self, columns):
        """Handle column selection changes."""
        self.state.set_columns(columns)
        
    def _on_data_loaded(self, data):
        """Handle state data loaded event."""
        # Update preview with original data
        self.preview_panel.update_preview(data, is_processed=False)
        
    def _on_pipeline_executed(self, result):
        """Handle pipeline execution completion."""
        self.preview_panel.update_preview(result.dataframe, is_processed=True)
        self.metrics_display.update_metrics(result.metrics)
        self.export_button.config(state='normal')
        
        exec_time = result.metrics.get('execution_time', 0)
        removed = result.metrics.get('total_removed', 0)
        self.status_bar.config(text=f"Pipeline executed in {exec_time:.3f}s - {removed} rows removed")
        
    def _on_preview_selection(self, selected_values):
        """Handle preview selection change."""
        # Optional: Show details of selected row
        if selected_values:
            self.status_bar.config(text=f"Selected: {', '.join(str(v) for v in selected_values[:3])}...")
            
    def _on_metric_click(self, metric_info):
        """Handle metric click event."""
        # Optional: Implement metric-specific actions
        pass
        
    def _run_pipeline(self):
        """Execute the data pipeline."""
        if not self.state.has_data:
            messagebox.showwarning("Warning", "Please load data first.")
            return
            
        try:
            self.status_bar.config(text="Running pipeline...")
            self.root.update()
            
            # Get current data with selected columns
            current_data = self.state.current_data[self.state.current_columns].copy() if self.state.current_columns else self.state.current_data.copy()
            
            result = self.pipeline_service.execute_pipeline(
                current_data,
                self.state.current_config
            )
            self.state.set_pipeline_result(result)
            
        except Exception as e:
            self.status_bar.config(text=f"Error: {str(e)}")
            messagebox.showerror("Pipeline Error", f"Failed to execute pipeline:\n{str(e)}")
            
    def _export_data(self):
        """Export processed data."""
        if not self.state.has_processed_data:
            messagebox.showwarning("Warning", "No processed data to export. Run pipeline first.")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("Excel files", "*.xlsx"),
                ("All files", "*.*")
            ],
            title="Save Processed Data"
        )
        
        if not filepath:
            return
            
        try:
            # Get the data to export
            export_data = self.state.pipeline_result.dataframe
            
            # Export based on file extension
            ext = Path(filepath).suffix.lower()
            if ext == '.xlsx':
                export_data.to_excel(filepath, index=False)
            else:
                # Default to CSV with configurable delimiter
                delimiter = self.state.current_config.default_delimiter
                export_data.to_csv(filepath, sep=delimiter, index=False, encoding='utf-8-sig')
                
            messagebox.showinfo("Success", f"Data exported successfully to:\n{filepath}")
            self.status_bar.config(text=f"Exported: {Path(filepath).name}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")
            self.status_bar.config(text="Export failed")
            
    def _menu_open_file(self):
        """Handle menu file open."""
        self.file_loader._load_file_dialog()
        
    def _menu_export(self):
        """Handle menu export."""
        self._export_data()
        
    def _menu_run_pipeline(self):
        """Handle menu run pipeline."""
        self._run_pipeline()
        
    def _menu_reset(self):
        """Handle menu reset."""
        self.state.reset()
        self.file_loader.clear()
        self.config_panel.set_config(AppConfig.get_default())
        self.column_editor.clear()
        self.preview_panel.clear()
        self.metrics_display.clear()
        self.export_button.config(state='disabled')
        self.notebook.tab(1, state='disabled')
        self.status_bar.config(text="Reset complete - Ready to load new data")
        
    def _menu_about(self):
        """Show about dialog."""
        about_text = """
        Tk Data Preparer - Professional Edition
        
        A modern tool for data cleaning, transformation, and preparation.
        
        Features:
        - Load Excel, CSV, and TXT files
        - Advanced data cleaning and normalization
        - Intelligent filtering and deduplication
        - Real-time preview and metrics
        - Professional export capabilities
        
        Version: 1.0.0
        Author: Lucas Ferreira
        """
        
        messagebox.showinfo("About Tk Data Preparer", about_text.strip())
        
    def run(self):
        """Start the application."""
        self.root.mainloop()

    def __del__(self):
        """Cleanup when application is destroyed."""
        if hasattr(self, 'state'):
            # Unsubscribe all callbacks to prevent memory leaks
            events = ['data_loaded', 'config_changed', 'columns_changed', 'pipeline_executed', 'reset']
            for event in events:
                callback_method = getattr(self, f'_on_{event}', None)
                if callback_method:
                    self.state.unsubscribe(event, callback_method)


def main():
    """Application entry point."""
    root = tk.Tk()
    app = TkDataPreparerApp(root)
    app.run()


if __name__ == "__main__":
    main()