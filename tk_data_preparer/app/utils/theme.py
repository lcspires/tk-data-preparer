"""
Theme and styling utilities for Tk Data Preparer.
"""

import tkinter as tk
from tkinter import ttk

# Color scheme
COLOR_SCHEME = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'light': '#ecf0f1',
    'dark': '#2c3e50'
}

# Style configuration
STYLES = {
    'font_family': 'Segoe UI',
    'font_size_normal': 10,
    'font_size_large': 12,
    'font_size_title': 14,
    'padding_small': 5,
    'padding_medium': 10,
    'padding_large': 15
}

def apply_theme(root):
    """Apply modern theme to the application."""
    style = ttk.Style()
    
    # Configure styles
    style.configure('TFrame', background=COLOR_SCHEME['light'])
    style.configure('TLabel', background=COLOR_SCHEME['light'], font=(STYLES['font_family'], STYLES['font_size_normal']))
    style.configure('TButton', font=(STYLES['font_family'], STYLES['font_size_normal']))
    style.configure('Accent.TButton', background=COLOR_SCHEME['accent'], foreground='white')
    
    # Configure notebook
    style.configure('TNotebook', background=COLOR_SCHEME['light'])
    style.configure('TNotebook.Tab', font=(STYLES['font_family'], STYLES['font_size_normal'], 'bold'))
    
    # Set window background
    root.configure(background=COLOR_SCHEME['light'])