"""
Modern tooltip implementation.
"""

import tkinter as tk

class ToolTip:
    """Enhanced tooltip with modern styling."""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        
    def enter(self, event=None):
        """Show tooltip on hover."""
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip, 
            text=self.text, 
            justify='left',
            background="#ffffe0", 
            relief='solid', 
            borderwidth=1,
            font=('TkDefaultFont', 9)
        )
        label.pack()
        
    def leave(self, event=None):
        """Hide tooltip."""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None