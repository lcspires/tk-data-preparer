"""
Configuration panel for pipeline settings.
Provides UI for configuring cleaning, filtering, and deduplication options.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Literal, Dict, Any
import tkinter.font as tkfont

from tk_data_preparer.core import AppConfig, CleanConfig, FilterConfig, DedupConfig


class ConfigPanel(ttk.LabelFrame):
    """Panel for configuring data processing pipeline."""
    
    def __init__(self, parent, on_config_change: Optional[Callable] = None):
        super().__init__(parent, text="⚙️ Pipeline Configuration", padding=10)
        self.on_config_change = on_config_change
        self.config = AppConfig.get_default()
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup configuration UI with notebook tabs."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='x', expand=True)
        
        # Create tabs for each configuration section
        self.cleaning_tab = ttk.Frame(self.notebook, padding=10)
        self.filtering_tab = ttk.Frame(self.notebook, padding=10)
        self.deduplication_tab = ttk.Frame(self.notebook, padding=10)
        self.presets_tab = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.cleaning_tab, text="🧹 Cleaning")
        self.notebook.add(self.filtering_tab, text="🔍 Filtering")
        self.notebook.add(self.deduplication_tab, text="🚫 Deduplication")
        self.notebook.add(self.presets_tab, text="💾 Presets")
        
        self._setup_cleaning_tab()
        self._setup_filtering_tab()
        self._setup_deduplication_tab()
        self._setup_presets_tab()
        
    def _setup_cleaning_tab(self):
        """Setup cleaning configuration options."""
        # Strip whitespace
        self.strip_var = tk.BooleanVar(value=self.config.pipeline.cleaning.strip)
        ttk.Checkbutton(self.cleaning_tab, text="Strip leading/trailing whitespace",
                       variable=self.strip_var, command=self._on_config_change).grid(row=0, column=0, sticky='w', pady=2)
        
        # Collapse whitespace
        self.collapse_var = tk.BooleanVar(value=self.config.pipeline.cleaning.collapse_whitespace)
        ttk.Checkbutton(self.cleaning_tab, text="Collapse internal whitespace",
                       variable=self.collapse_var, command=self._on_config_change).grid(row=1, column=0, sticky='w', pady=2)
        
        # Case conversion
        ttk.Label(self.cleaning_tab, text="Case conversion:").grid(row=2, column=0, sticky='w', pady=(10, 2))
        self.case_var = tk.StringVar(value=self.config.pipeline.cleaning.case or 'none')
        case_frame = ttk.Frame(self.cleaning_tab)
        case_frame.grid(row=3, column=0, sticky='w', pady=2)
        ttk.Radiobutton(case_frame, text="None", variable=self.case_var, value='none', 
                       command=self._on_config_change).pack(side='left')
        ttk.Radiobutton(case_frame, text="Lowercase", variable=self.case_var, value='lower', 
                       command=self._on_config_change).pack(side='left', padx=5)
        ttk.Radiobutton(case_frame, text="Uppercase", variable=self.case_var, value='upper', 
                       command=self._on_config_change).pack(side='left')
        ttk.Radiobutton(case_frame, text="Title Case", variable=self.case_var, value='title', 
                       command=self._on_config_change).pack(side='left', padx=5)
        
        # Unicode normalization
        ttk.Label(self.cleaning_tab, text="Unicode normalization:").grid(row=4, column=0, sticky='w', pady=(10, 2))
        self.unicode_var = tk.StringVar(value=self.config.pipeline.cleaning.unicode_normalization or 'none')
        unicode_combo = ttk.Combobox(self.cleaning_tab, textvariable=self.unicode_var, 
                                    values=['none', 'NFC', 'NFD', 'NFKC', 'NFKD'], state='readonly', width=10)
        unicode_combo.grid(row=5, column=0, sticky='w', pady=2)
        unicode_combo.bind('<<ComboboxSelected>>', lambda e: self._on_config_change())
        
        # Empty to NA
        self.empty_na_var = tk.BooleanVar(value=self.config.pipeline.cleaning.empty_to_na)
        ttk.Checkbutton(self.cleaning_tab, text="Convert empty strings to NA",
                       variable=self.empty_na_var, command=self._on_config_change).grid(row=6, column=0, sticky='w', pady=2)
        
    def _setup_filtering_tab(self):
        """Setup filtering configuration options."""
        # Enable filtering
        self.filtering_enabled_var = tk.BooleanVar(value=self.config.pipeline.filtering is not None)
        ttk.Checkbutton(self.filtering_tab, text="Enable filtering",
                       variable=self.filtering_enabled_var, command=self._toggle_filtering).grid(row=0, column=0, sticky='w', pady=2)
        
        # Min length
        ttk.Label(self.filtering_tab, text="Minimum character length:").grid(row=1, column=0, sticky='w', pady=(10, 2))
        self.min_length_var = tk.StringVar(value=str(self.config.pipeline.filtering.min_length if self.config.pipeline.filtering else 3))
        min_length_spin = ttk.Spinbox(self.filtering_tab, from_=1, to=100, textvariable=self.min_length_var,
                                     width=5, command=self._on_config_change)
        min_length_spin.grid(row=2, column=0, sticky='w', pady=2)
        min_length_spin.bind('<KeyRelease>', lambda e: self._on_config_change())
        
        # Drop NA
        self.drop_na_var = tk.BooleanVar(value=self.config.pipeline.filtering.drop_na if self.config.pipeline.filtering else True)
        ttk.Checkbutton(self.filtering_tab, text="Remove rows with NA values",
                       variable=self.drop_na_var, command=self._on_config_change).grid(row=3, column=0, sticky='w', pady=2)
        
        # Initially disable filtering widgets if not enabled
        self._toggle_filtering_widgets(self.filtering_enabled_var.get())
        
    def _setup_deduplication_tab(self):
        """Setup deduplication configuration options."""
        # Enable deduplication
        self.deduplication_enabled_var = tk.BooleanVar(value=self.config.pipeline.deduplication is not None)
        ttk.Checkbutton(self.deduplication_tab, text="Enable deduplication",
                       variable=self.deduplication_enabled_var, command=self._toggle_deduplication).grid(row=0, column=0, sticky='w', pady=2)
        
        # Keep strategy
        ttk.Label(self.deduplication_tab, text="Keep strategy:").grid(row=1, column=0, sticky='w', pady=(10, 2))
        self.keep_var = tk.StringVar(value=self.config.pipeline.deduplication.keep if self.config.pipeline.deduplication else 'first')
        keep_combo = ttk.Combobox(self.deduplication_tab, textvariable=self.keep_var,
                                 values=['first', 'last', 'none'], state='readonly', width=10)
        keep_combo.grid(row=2, column=0, sticky='w', pady=2)
        keep_combo.bind('<<ComboboxSelected>>', lambda e: self._on_config_change())
        
        # Case sensitive
        self.case_sensitive_var = tk.BooleanVar(value=self.config.pipeline.deduplication.case_sensitive if self.config.pipeline.deduplication else False)
        ttk.Checkbutton(self.deduplication_tab, text="Case sensitive comparison",
                       variable=self.case_sensitive_var, command=self._on_config_change).grid(row=3, column=0, sticky='w', pady=2)
        
        # Unicode normalization
        self.normalize_unicode_var = tk.BooleanVar(value=self.config.pipeline.deduplication.normalize_unicode if self.config.pipeline.deduplication else False)
        ttk.Checkbutton(self.deduplication_tab, text="Unicode normalization before deduplication",
                       variable=self.normalize_unicode_var, command=self._on_config_change).grid(row=4, column=0, sticky='w', pady=2)
        
        # Initially disable deduplication widgets if not enabled
        self._toggle_deduplication_widgets(self.deduplication_enabled_var.get())
        
    def _setup_presets_tab(self):
        """Setup configuration presets."""
        ttk.Label(self.presets_tab, text="Quick configuration presets:").pack(anchor='w', pady=(0, 10))
        
        presets = [
            ("📊 Customer Data", "customer_data"),
            ("📦 Product Catalog", "product_catalog"), 
            ("🧹 Minimal Cleaning", "minimal"),
            ("⚙️ Default", "default")
        ]
        
        for preset_name, preset_key in presets:
            ttk.Button(self.presets_tab, text=preset_name,
                      command=lambda k=preset_key: self._apply_preset(k)).pack(fill='x', pady=2)
        
    def _toggle_filtering(self):
        """Toggle filtering enabled state."""
        enabled = self.filtering_enabled_var.get()
        self._toggle_filtering_widgets(enabled)
        self._on_config_change()
        
    def _toggle_filtering_widgets(self, enabled: bool):
        """Enable/disable filtering widgets."""
        state = 'normal' if enabled else 'disabled'
        for widget in self.filtering_tab.winfo_children()[1:]:  # Skip the enable checkbox
            if hasattr(widget, 'configure'):
                widget.configure(state=state)
        
    def _toggle_deduplication(self):
        """Toggle deduplication enabled state."""
        enabled = self.deduplication_enabled_var.get()
        self._toggle_deduplication_widgets(enabled)
        self._on_config_change()
        
    def _toggle_deduplication_widgets(self, enabled: bool):
        """Enable/disable deduplication widgets."""
        state = 'normal' if enabled else 'disabled'
        for widget in self.deduplication_tab.winfo_children()[1:]:  # Skip the enable checkbox
            if hasattr(widget, 'configure'):
                widget.configure(state=state)
                
    def _apply_preset(self, preset_key: str):
        """Apply configuration preset."""
        from tk_data_preparer.core import PRESET_CONFIGS
        
        if preset_key == 'default':
            self.config = AppConfig.get_default()
        else:
            self.config = PRESET_CONFIGS[preset_key]
        
        self._update_ui_from_config()
        self._on_config_change()
        
    def _update_ui_from_config(self):
        """Update UI from current config."""
        # Cleaning
        self.strip_var.set(self.config.pipeline.cleaning.strip)
        self.collapse_var.set(self.config.pipeline.cleaning.collapse_whitespace)
        self.case_var.set(self.config.pipeline.cleaning.case or 'none')
        self.unicode_var.set(self.config.pipeline.cleaning.unicode_normalization or 'none')
        self.empty_na_var.set(self.config.pipeline.cleaning.empty_to_na)
        
        # Filtering
        filtering_enabled = self.config.pipeline.filtering is not None
        self.filtering_enabled_var.set(filtering_enabled)
        if self.config.pipeline.filtering:
            self.min_length_var.set(str(self.config.pipeline.filtering.min_length))
            self.drop_na_var.set(self.config.pipeline.filtering.drop_na)
        self._toggle_filtering_widgets(filtering_enabled)
        
        # Deduplication
        deduplication_enabled = self.config.pipeline.deduplication is not None
        self.deduplication_enabled_var.set(deduplication_enabled)
        if self.config.pipeline.deduplication:
            self.keep_var.set(self.config.pipeline.deduplication.keep)
            self.case_sensitive_var.set(self.config.pipeline.deduplication.case_sensitive)
            self.normalize_unicode_var.set(self.config.pipeline.deduplication.normalize_unicode)
        self._toggle_deduplication_widgets(deduplication_enabled)
        
    def _on_config_change(self):
        """Handle configuration change and notify parent."""
        self._update_config_from_ui()
        if self.on_config_change:
            self.on_config_change(self.config)
            
    def _update_config_from_ui(self):
        """Update config from UI values."""
        # Cleaning config
        cleaning_config = CleanConfig(
            strip=self.strip_var.get(),
            collapse_whitespace=self.collapse_var.get(),
            case=self.case_var.get() if self.case_var.get() != 'none' else None,
            unicode_normalization=self.unicode_var.get() if self.unicode_var.get() != 'none' else None,
            empty_to_na=self.empty_na_var.get()
        )
        
        # Filtering config
        filtering_config = None
        if self.filtering_enabled_var.get():
            try:
                min_length = int(self.min_length_var.get())
            except ValueError:
                min_length = 3
            filtering_config = FilterConfig(
                min_length=min_length,
                drop_na=self.drop_na_var.get()
            )
        
        # Deduplication config
        deduplication_config = None
        if self.deduplication_enabled_var.get():
            deduplication_config = DedupConfig(
                keep=self.keep_var.get(),
                case_sensitive=self.case_sensitive_var.get(),
                normalize_unicode=self.normalize_unicode_var.get()
            )
        
        # Update main config
        self.config.pipeline.cleaning = cleaning_config
        self.config.pipeline.filtering = filtering_config
        self.config.pipeline.deduplication = deduplication_config
        
    def get_config(self) -> AppConfig:
        """Get current configuration."""
        self._update_config_from_ui()
        return self.config
        
    def set_config(self, config: AppConfig):
        """Set configuration from external source."""
        self.config = config
        self._update_ui_from_config()