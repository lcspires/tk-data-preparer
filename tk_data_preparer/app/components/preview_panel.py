"""
Preview panel for displaying data in a scrollable table view.
Shows both original and processed data with pagination and search.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
import pandas as pd


class PreviewPanel(ttk.LabelFrame):
    """Panel for data preview with pagination and search."""
    
    def __init__(self, parent, on_selection_change: Optional[Callable] = None):
        super().__init__(parent, text="👀 Data Preview", padding=10)
        self.on_selection_change = on_selection_change
        self.current_data: Optional[pd.DataFrame] = None
        self.current_page = 1
        self.rows_per_page = 10
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup preview UI with controls and treeview."""
        # Controls frame
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Search controls
        ttk.Label(controls_frame, text="Search:").pack(side='left', padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(controls_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side='left', padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self._on_search)
        
        # Pagination controls
        pagination_frame = ttk.Frame(controls_frame)
        pagination_frame.pack(side='right')
        
        ttk.Button(pagination_frame, text="◀", width=3, 
                  command=self._previous_page).pack(side='left', padx=2)
        
        self.page_label = ttk.Label(pagination_frame, text="Page 1 of 1", width=12)
        self.page_label.pack(side='left', padx=5)
        
        ttk.Button(pagination_frame, text="▶", width=3, 
                  command=self._next_page).pack(side='left', padx=2)
        
        # Rows per page
        ttk.Label(controls_frame, text="Rows:").pack(side='right', padx=(10, 5))
        self.rows_var = tk.StringVar(value=str(self.rows_per_page))
        rows_spin = ttk.Spinbox(controls_frame, from_=5, to=50, textvariable=self.rows_var,
                               width=5, command=self._on_rows_change)
        rows_spin.pack(side='right')
        rows_spin.bind('<KeyRelease>', lambda e: self._on_rows_change())
        
        # Treeview for data display
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill='both', expand=True)
        
        self.tree = ttk.Treeview(tree_frame, show='headings', selectmode='browse')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for tree and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Status bar
        self.status_bar = ttk.Label(self, text="No data loaded", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill='x', pady=(10, 0))
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
        
    def update_preview(self, data: pd.DataFrame, is_processed: bool = False):
        """Update preview with new data."""
        self.current_data = data
        self.current_page = 1
        
        self._clear_tree()
        self._setup_tree_columns(data.columns.tolist())
        self._load_current_page()
        
        status_text = f"Showing {len(data)} rows"
        if is_processed:
            status_text += " (processed)"
        self.status_bar.config(text=status_text)
        
    def _setup_tree_columns(self, columns: list):
        """Setup treeview columns based on data columns."""
        self.tree['columns'] = columns
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=80, stretch=True)
            
    def _clear_tree(self):
        """Clear all items from treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def _load_current_page(self):
        """Load current page of data into treeview."""
        if self.current_data is None or self.current_data.empty:
            return
            
        # Calculate pagination
        total_rows = len(self.current_data)
        total_pages = max(1, (total_rows + self.rows_per_page - 1) // self.rows_per_page)
        self.current_page = min(max(1, self.current_page), total_pages)
        
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, total_rows)
        
        # Update page info
        self.page_label.config(text=f"Page {self.current_page} of {total_pages}")
        
        # Load page data
        page_data = self.current_data.iloc[start_idx:end_idx]
        
        for _, row in page_data.iterrows():
            values = [self._format_value(val) for val in row]
            self.tree.insert('', 'end', values=values)
            
    def _format_value(self, value) -> str:
        """Format value for display in treeview."""
        if pd.isna(value):
            return "NULL"
        elif isinstance(value, float):
            return f"{value:.2f}"
        elif isinstance(value, str) and len(value) > 50:
            return value[:47] + "..."
        else:
            return str(value)
            
    def _previous_page(self):
        """Navigate to previous page."""
        if self.current_data is None:
            return
            
        total_pages = max(1, (len(self.current_data) + self.rows_per_page - 1) // self.rows_per_page)
        if self.current_page > 1:
            self.current_page -= 1
            self._refresh_preview()
            
    def _next_page(self):
        """Navigate to next page."""
        if self.current_data is None:
            return
            
        total_pages = max(1, (len(self.current_data) + self.rows_per_page - 1) // self.rows_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self._refresh_preview()
            
    def _on_rows_change(self):
        """Handle rows per page change."""
        try:
            new_rows = int(self.rows_var.get())
            if 5 <= new_rows <= 50:
                self.rows_per_page = new_rows
                self.current_page = 1
                self._refresh_preview()
        except ValueError:
            pass
            
    def _on_search(self, event=None):
        """Handle search functionality."""
        search_term = self.search_var.get().lower()
        
        if not search_term or self.current_data is None:
            self._refresh_preview()
            return
            
        # Filter data based on search term
        filtered_data = self.current_data.copy()
        for col in filtered_data.columns:
            if filtered_data[col].dtype == 'object':
                filtered_data = filtered_data[filtered_data[col].astype(str).str.lower().str.contains(search_term, na=False)]
                
        self._clear_tree()
        self._load_filtered_preview(filtered_data)
        
    def _load_filtered_preview(self, filtered_data: pd.DataFrame):
        """Load filtered data into preview."""
        if filtered_data.empty:
            self.tree.insert('', 'end', values=['No matching records found'])
            return
            
        total_rows = len(filtered_data)
        total_pages = max(1, (total_rows + self.rows_per_page - 1) // self.rows_per_page)
        self.current_page = min(max(1, self.current_page), total_pages)
        
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, total_rows)
        
        self.page_label.config(text=f"Page {self.current_page} of {total_pages} (Filtered)")
        
        page_data = filtered_data.iloc[start_idx:end_idx]
        for _, row in page_data.iterrows():
            values = [self._format_value(val) for val in row]
            self.tree.insert('', 'end', values=values)
            
    def _refresh_preview(self):
        """Refresh preview with current settings."""
        self._clear_tree()
        
        if self.search_var.get():
            self._on_search()
        else:
            self._load_current_page()
            
    def _on_tree_select(self, event):
        """Handle treeview selection event."""
        selection = self.tree.selection()
        if selection and self.on_selection_change:
            item = self.tree.item(selection[0])
            self.on_selection_change(item['values'])
            
    def clear(self):
        """Clear preview panel."""
        self.current_data = None
        self._clear_tree()
        self.tree['columns'] = []
        self.status_bar.config(text="No data loaded")
        self.page_label.config(text="Page 1 of 1")
        self.search_var.set("")
        
    def get_current_page_data(self) -> Optional[pd.DataFrame]:
        """Get currently displayed page data."""
        if self.current_data is None:
            return None
            
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, len(self.current_data))
        return self.current_data.iloc[start_idx:end_idx].copy()