import tkinter as tk

class ToolTip:
    """
    Cria um tooltip (dica em balão) para widgets Tkinter.

    Uso:
    -------
    button = tk.Button(root, text="Clique aqui")
    ToolTip(button, "Este botão faz X, Y e Z")
    """

    def __init__(self, widget, text="widget info"):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self._show_tip)
        self.widget.bind("<Leave>", self._hide_tip)

    def _show_tip(self, event=None):
        """Exibe o tooltip próximo ao widget."""
        if self.tip_window or not self.text:
            return

        x, y, _, cy = self.widget.bbox("insert") if self.widget.bbox("insert") else (0, 0, 0, 0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # remove bordas
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=4, ipady=2)

    def _hide_tip(self, event=None):
        """Esconde o tooltip."""
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()
