"""
Column editor panel for selecting, reordering, and managing data columns.
Provides drag-and-drop functionality for intuitive column management.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional, Callable
import tkinter.dnd as dnd


class ColumnEditorPanel(ttk.LabelFrame):
    """Panel for column selection and reordering."""
    
    def __init__(self, parent, on_columns_change: Optional[Callable] = None):
        super().__init__(parent, text="📊 Column Selection & Ordering", padding=10)
        self.on_columns_change = on_columns_change
        self.available_columns: List[str] = []
        self.selected_columns: List[str] = []
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup column editor UI with two listboxes and controls."""
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True)
        
        # Available columns section
        available_frame = ttk.LabelFrame(main_frame, text="Available Columns")
        available_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        self.available_listbox = tk.Listbox(available_frame, selectmode=tk.EXTENDED, 
                                           height=8, exportselection=False)
        self.available_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.available_listbox.bind('<<ListboxSelect>>', self._on_available_select)
        self.available_listbox.bind('<Double-Button-1>', self._add_selected_columns)
        
        available_scrollbar = ttk.Scrollbar(available_frame, orient='vertical', 
                                           command=self.available_listbox.yview)
        available_scrollbar.pack(side='right', fill='y')
        self.available_listbox.configure(yscrollcommand=available_scrollbar.set)
        
        # Selected columns section
        selected_frame = ttk.LabelFrame(main_frame, text="Selected Columns (Drag to reorder)")
        selected_frame.grid(row=0, column=2, sticky='nsew', padx=(5, 0))
        
        self.selected_listbox = tk.Listbox(selected_frame, selectmode=tk.EXTENDED,
                                          height=8, exportselection=False)
        self.selected_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.selected_listbox.bind('<<ListboxSelect>>', self._on_selected_select)
        self.selected_listbox.bind('<Double-Button-1>', self._remove_selected_columns)
        
        # Enable drag and drop for reordering
        self._enable_drag_and_drop()
        
        selected_scrollbar = ttk.Scrollbar(selected_frame, orient='vertical',
                                          command=self.selected_listbox.yview)
        selected_scrollbar.pack(side='right', fill='y')
        self.selected_listbox.configure(yscrollcommand=selected_scrollbar.set)
        
        # Control buttons frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=0, column=1, sticky='ns', padx=5)
        
        ttk.Button(controls_frame, text="→ Add", 
                  command=self._add_selected_columns, width=10).pack(pady=2)
        ttk.Button(controls_frame, text="← Remove", 
                  command=self._remove_selected_columns, width=10).pack(pady=2)
        ttk.Button(controls_frame, text="↑ Move Up", 
                  command=self._move_up, width=10).pack(pady=2)
        ttk.Button(controls_frame, text="↓ Move Down", 
                  command=self._move_down, width=10).pack(pady=2)
        ttk.Button(controls_frame, text="🔄 Reset", 
                  command=self._reset_columns, width=10).pack(pady=20)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
    def _enable_drag_and_drop(self):
        """Enable drag and drop functionality for reordering."""
        self.selected_listbox.bind('<ButtonPress-1>', self._on_drag_start)
        self.selected_listbox.bind('<B1-Motion>', self._on_drag_motion)
        self.selected_listbox.bind('<ButtonRelease-1>', self._on_drag_release)
        self.drag_data = {'index': None, 'y': 0}
        
    def _on_drag_start(self, event):
        """Handle drag start event."""
        index = self.selected_listbox.nearest(event.y)
        if index >= 0:
            self.drag_data['index'] = index
            self.drag_data['y'] = event.y
            
    def _on_drag_motion(self, event):
        """Handle drag motion event."""
        if self.drag_data['index'] is not None:
            # Visual feedback during drag
            pass
            
    def _on_drag_release(self, event):
        """Handle drag release event for reordering."""
        if self.drag_data['index'] is not None:
            source_index = self.drag_data['index']
            target_index = self.selected_listbox.nearest(event.y)
            
            if 0 <= source_index < self.selected_listbox.size() and 0 <= target_index < self.selected_listbox.size():
                self._reorder_columns(source_index, target_index)
            
            self.drag_data['index'] = None
            
    def _reorder_columns(self, source_index: int, target_index: int):
        """Reorder columns by moving item from source to target index."""
        if source_index == target_index:
            return
            
        item = self.selected_columns[source_index]
        self.selected_columns.pop(source_index)
        self.selected_columns.insert(target_index, item)
        
        self._refresh_selected_listbox()
        self._notify_columns_change()
        
    def set_columns(self, columns: List[str]):
        """Set available columns and reset selection."""
        self.available_columns = columns.copy()
        self.selected_columns = columns.copy()  # Start with all columns selected
        
        self._refresh_available_listbox()
        self._refresh_selected_listbox()
        self._notify_columns_change()
        
    def get_selected_columns(self) -> List[str]:
        """Get currently selected columns in order."""
        return self.selected_columns.copy()
        
    def _refresh_available_listbox(self):
        """Refresh available columns listbox."""
        self.available_listbox.delete(0, tk.END)
        available_cols = [col for col in self.available_columns if col not in self.selected_columns]
        
        for col in available_cols:
            self.available_listbox.insert(tk.END, col)
            
    def _refresh_selected_listbox(self):
        """Refresh selected columns listbox."""
        self.selected_listbox.delete(0, tk.END)
        for col in self.selected_columns:
            self.selected_listbox.insert(tk.END, col)
            
    def _on_available_select(self, event):
        """Handle selection in available listbox."""
        # Clear selection in selected listbox
        self.selected_listbox.selection_clear(0, tk.END)
        
    def _on_selected_select(self, event):
        """Handle selection in selected listbox."""
        # Clear selection in available listbox
        self.available_listbox.selection_clear(0, tk.END)
        
    def _add_selected_columns(self, event=None):
        """Add selected columns from available to selected."""
        selected_indices = self.available_listbox.curselection()
        if not selected_indices:
            return
            
        columns_to_add = []
        for index in selected_indices:
            col = self.available_listbox.get(index)
            columns_to_add.append(col)
            
        # Add to selected columns and refresh
        self.selected_columns.extend(columns_to_add)
        self._refresh_available_listbox()
        self._refresh_selected_listbox()
        self._notify_columns_change()
        
    def _remove_selected_columns(self, event=None):
        """Remove selected columns from selected list."""
        selected_indices = self.selected_listbox.curselection()
        if not selected_indices:
            return
            
        # Remove in reverse order to avoid index issues
        for index in reversed(selected_indices):
            if 0 <= index < len(self.selected_columns):
                self.selected_columns.pop(index)
                
        self._refresh_available_listbox()
        self._refresh_selected_listbox()
        self._notify_columns_change()
        
    def _move_up(self):
        """Move selected columns up in the list."""
        selected_indices = list(self.selected_listbox.curselection())
        if not selected_indices or selected_indices[0] == 0:
            return
            
        # Move each selected item up
        for index in selected_indices:
            if index > 0:
                self.selected_columns[index], self.selected_columns[index-1] = \
                self.selected_columns[index-1], self.selected_columns[index]
                
        self._refresh_selected_listbox()
        
        # Reselect moved items
        for new_index in [i-1 for i in selected_indices]:
            self.selected_listbox.selection_set(new_index)
            
        self._notify_columns_change()
        
    def _move_down(self):
        """Move selected columns down in the list."""
        selected_indices = list(self.selected_listbox.curselection())
        if not selected_indices or selected_indices[-1] == len(self.selected_columns) - 1:
            return
            
        # Move each selected item down (in reverse order)
        for index in reversed(selected_indices):
            if index < len(self.selected_columns) - 1:
                self.selected_columns[index], self.selected_columns[index+1] = \
                self.selected_columns[index+1], self.selected_columns[index]
                
        self._refresh_selected_listbox()
        
        # Reselect moved items
        for new_index in [i+1 for i in selected_indices]:
            self.selected_listbox.selection_set(new_index)
            
        self._notify_columns_change()
        
    def _reset_columns(self):
        """Reset to all available columns."""
        self.selected_columns = self.available_columns.copy()
        self._refresh_available_listbox()
        self._refresh_selected_listbox()
        self._notify_columns_change()
        
    def _notify_columns_change(self):
        """Notify parent about column changes."""
        if self.on_columns_change:
            self.on_columns_change(self.selected_columns)
            
    def clear(self):
        """Clear all columns."""
        self.available_columns = []
        self.selected_columns = []
        self.available_listbox.delete(0, tk.END)
        self.selected_listbox.delete(0, tk.END)