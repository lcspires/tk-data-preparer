# tk_data_preparer/tooltip.py
import tkinter as tk


class ToolTip:
    def __init__(self, widget, texto="Tooltip"):
        self.widget = widget
        self.texto = texto
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

        # Eventos do mouse
        self.widget.bind("<Enter>", self._enter)
        self.widget.bind("<Leave>", self._leave)

    def _enter(self, event=None):
        self._mostrar_tooltip()

    def _leave(self, event=None):
        self._esconder_tooltip()

    def _mostrar_tooltip(self):
        """Cria uma pequena janela com o texto."""
        if self.tipwindow or not self.texto:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # remove borda
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.texto,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("tahoma", 9, "normal"),
            padx=4,
            pady=2,
        )
        label.pack(ipadx=1)

    def _esconder_tooltip(self):
        """Fecha a janela do tooltip."""
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
