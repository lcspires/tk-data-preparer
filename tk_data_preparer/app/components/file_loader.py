"""
File loader component for loading various data formats.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, Optional, Tuple
import pandas as pd
from pathlib import Path

# ✅ CORRIGIDO: Importação absoluta em vez de relativa
from tk_data_preparer.app.services.file_service import FileService


class FileLoaderPanel(ttk.LabelFrame):
    """Panel for loading Excel, CSV, and TXT files."""
    
    def __init__(self, parent, on_file_loaded: Optional[Callable] = None):
        super().__init__(parent, text="📁 Data Source", padding=10)
        self.on_file_loaded = on_file_loaded
        self.file_service = FileService()
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup file loader UI."""
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="📊 Load Excel", command=self._load_excel, width=15).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="📝 Load CSV", command=self._load_csv, width=15).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="📄 Load TXT", command=self._load_txt, width=15).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="🔍 Auto Detect", command=self._load_any, width=15).pack(side='left', padx=2)
        
        # File info display
        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(fill='x', pady=5)
        
        self.status_label = ttk.Label(self.info_frame, text="No file loaded", font=('Arial', 9))
        self.status_label.pack(anchor='w')
        
        self.details_label = ttk.Label(self.info_frame, text="", font=('Arial', 8), foreground='gray')
        self.details_label.pack(anchor='w')
        
    def _load_excel(self):
        """Load Excel file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xls *.xlsx"), ("All files", "*.*")]
        )
        if filepath:
            self._load_file(filepath)
            
    def _load_csv(self):
        """Load CSV file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filepath:
            self._load_file(filepath)
            
    def _load_txt(self):
        """Load TXT file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            self._load_file(filepath)
            
    def _load_any(self):
        """Load any supported file with auto-detection."""
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("Excel files", "*.xls *.xlsx"),
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if filepath:
            self._load_file(filepath)
            
    def _load_file(self, filepath: str):
        """Load file using file service with auto-detection."""
        try:
            # Mostra informações do arquivo antes de carregar
            file_info = self.file_service.detect_file_info(filepath)
            self.details_label.config(text=f"Detected: {file_info['extension']} • {file_info['size_mb']}MB • {file_info.get('encoding', 'unknown')}")
            
            # Carrega o arquivo
            df, file_type = self.file_service.load_file(filepath)
            
            if self.on_file_loaded:
                self.on_file_loaded(df, filepath)
                
            self.status_label.config(text=f"✅ Loaded: {Path(filepath).name} ({len(df)} rows, {file_type})")
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load file:\n{str(e)}")
            self.status_label.config(text="❌ Load failed")
            self.details_label.config(text="")
            
    def clear(self):
        """Clear file loader state."""
        self.status_label.config(text="No file loaded")
        self.details_label.config(text="")