import tkinter as tk


class ToolTip:
    """
    Classe para exibir uma tooltip (dica de ajuda) quando o mouse passa sobre um widget.
    """

    def __init__(self, widget, texto="Tooltip text"):
        self.widget = widget
        self.texto = texto
        self.tooltip_window = None
        widget.bind("<Enter>", self._mostrar)
        widget.bind("<Leave>", self._esconder)

    def _mostrar(self, event=None):
        if self.tooltip_window or not self.texto:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.texto,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", "9", "normal"),
            wraplength=250,
        )
        label.pack(ipadx=4, ipady=2)

    def _esconder(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
