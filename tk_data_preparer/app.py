"""
Tkinter Application for Preparing and Converting Excel (.xls, .xlsx), CSV, and TXT Files into Formatted TXT Files.

Features:
- Loads Excel, CSV, or TXT files.
- Allows selection and organization of the loaded file’s columns.
- Removes excess whitespace from all selected columns.
- Filters rows based on minimum character length in the first column.
- Removes duplicates based on the first column.
- Exports the final result as a user-selected delimited TXT file.
- Provides tooltip guidance and preview of the first few rows.

Author: Lucas Ferreira
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
from tk_data_preparer.logic import (
    limpar_espacos_em_colunas,
    remover_duplicatas,
    filtrar_primeira_coluna_por_tamanho
)
from tk_data_preparer.tooltip import ToolTip

# Define general styles
STYLES = {
    "btn_bg": "#4CAF50",
    "btn_fg": "white",
    "btn_font": ("Arial", 12, "bold"),
    "label_font": ("Arial", 10),
    "title_font": ("Arial", 14, "bold")
}


def tentar_leitura_csv_variavel_sep(caminho_arquivo):
    """Attempts to read CSV/TXT with common separators and encodings."""
    sep_list = [';', ',', '\t']
    for sep in sep_list:
        try:
            return pd.read_csv(caminho_arquivo, sep=sep, quotechar='"', encoding='utf-8', on_bad_lines='skip')
        except UnicodeDecodeError:
            try:
                return pd.read_csv(caminho_arquivo, sep=sep, quotechar='"', encoding='latin1', on_bad_lines='skip')
            except Exception:
                continue
        except Exception:
            continue
    raise Exception("Cannot read file with standard separators.")


class UnifiedApp:
    def __init__(self, root):
        self.root = root
        self.df = None
        self.total_espacos_removidos = 0
        self.linhas_removidas_por_tamanho = 0
        self.total_duplicatas_removidas = 0
        self.delimiter = ";"
        self._build_ui()

    def _build_ui(self):
        self.root.title("Tk Data Preparer: XLS/CSV → TXT")
        self.root.geometry("700x650")

        # File selection
        frame_file = tk.Frame(self.root, pady=10)
        frame_file.pack(fill="x")
        tk.Button(frame_file, text="Select File", font=STYLES["btn_font"],
                  bg=STYLES["btn_bg"], fg=STYLES["btn_fg"], command=self.selecionar_arquivo).pack(side="left", padx=5)
        self.label_resultado = tk.Label(frame_file, text="", font=STYLES["label_font"], fg="blue")
        self.label_resultado.pack(side="left", padx=10)

        # Min length and delimiter
        frame_config = tk.Frame(self.root, pady=5)
        frame_config.pack(fill="x")
        tk.Label(frame_config, text="Min characters in first column:", font=STYLES["label_font"]).pack(side="left")
        self.spin_min_len = tk.Spinbox(frame_config, from_=1, to=100, width=5)
        self.spin_min_len.pack(side="left", padx=5)
        self.spin_min_len.delete(0, "end")
        self.spin_min_len.insert(0, "6")

        tk.Label(frame_config, text="TXT delimiter:", font=STYLES["label_font"]).pack(side="left", padx=(20, 5))
        self.delim_var = tk.StringVar(value=";")
        tk.OptionMenu(frame_config, self.delim_var, ";", ",", "\t").pack(side="left")

        # Info tooltip
        self.icone_info = tk.Label(self.root, text="ℹ️", font=("Arial", 14), cursor="question_arrow")
        self.icone_info.pack_forget()
        texto_tooltip = (
            "Select an Excel (.xls/.xlsx), CSV or TXT file.\n"
            "Reorder and select columns, then generate a TXT.\n"
            "Removes extra spaces and filters rows by first column length."
        )
        self.tooltip = ToolTip(self.icone_info, texto_tooltip)

        # Columns selection
        self.listbox_colunas = tk.Listbox(self.root, selectmode=tk.EXTENDED, width=50, height=10)
        self.listbox_colunas.pack(pady=10)

        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=5)
        tk.Button(frame_botoes, text="↑ Move Up", command=self.mover_cima).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame_botoes, text="↓ Move Down", command=self.mover_baixo).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_botoes, text="✖ Remove Selected", command=self.remover_colunas, fg="red").grid(row=0, column=2, padx=5)
        tk.Button(frame_botoes, text="Reset", command=self.reset_app).grid(row=0, column=3, padx=5)

        # Preview tree
        self.tree_preview = ttk.Treeview(self.root, columns=[], show="headings", height=5)
        self.tree_preview.pack(pady=10, fill="x")

        # Status
        self.status_label = tk.Label(self.root, text="", font=STYLES["label_font"], fg="green")
        self.status_label.pack(pady=(0, 10))

        # Generate button
        tk.Button(self.root, text="Generate TXT", font=STYLES["btn_font"],
                  bg=STYLES["btn_bg"], fg=STYLES["btn_fg"], command=self.gerar_txt).pack(pady=10)

    # ---------------- File Handling ---------------- #
    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Select Excel, CSV or TXT file",
            filetypes=[("Excel files", "*.xls *.xlsx"), ("CSV", "*.csv"), ("TXT", "*.txt"), ("All files", "*.*")]
        )
        if not caminho_arquivo:
            self.label_resultado.config(text="No file selected.")
            self.icone_info.pack_forget()
            return

        ext = os.path.splitext(caminho_arquivo)[1].lower()
        try:
            if ext in ['.xls', '.xlsx']:
                self.df = pd.read_excel(caminho_arquivo)
            elif ext in ['.csv', '.txt']:
                self.df = tentar_leitura_csv_variavel_sep(caminho_arquivo)
            else:
                raise Exception("Unsupported file type.")
            self.label_resultado.config(text=f"Loaded: {os.path.basename(caminho_arquivo)}")
            self._carregar_colunas(self.df.columns.tolist())
            self.icone_info.pack(pady=(0, 10))
            self._update_preview()
            self.total_espacos_removidos = 0
            self.linhas_removidas_por_tamanho = 0
            self.total_duplicatas_removidas = 0
            self._atualizar_tooltip()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{e}")

    def _carregar_colunas(self, colunas):
        self.listbox_colunas.delete(0, tk.END)
        for col in colunas:
            self.listbox_colunas.insert(tk.END, col)

    # ---------------- Column Operations ---------------- #
    def mover_cima(self):
        selecionados = self.listbox_colunas.curselection()
        for index in selecionados:
            if index == 0:
                continue
            texto = self.listbox_colunas.get(index)
            acima = self.listbox_colunas.get(index - 1)
            self.listbox_colunas.delete(index - 1, index)
            self.listbox_colunas.insert(index - 1, texto)
            self.listbox_colunas.insert(index, acima)
            self.listbox_colunas.selection_set(index - 1)
            self.listbox_colunas.selection_clear(index)
        self._update_preview()

    def mover_baixo(self):
        selecionados = self.listbox_colunas.curselection()
        count = self.listbox_colunas.size()
        for index in reversed(selecionados):
            if index == count - 1:
                continue
            texto = self.listbox_colunas.get(index)
            abaixo = self.listbox_colunas.get(index + 1)
            self.listbox_colunas.delete(index, index + 1)
            self.listbox_colunas.insert(index, abaixo)
            self.listbox_colunas.insert(index + 1, texto)
            self.listbox_colunas.selection_set(index + 1)
            self.listbox_colunas.selection_clear(index)
        self._update_preview()

    def remover_colunas(self):
        selecionados = self.listbox_colunas.curselection()
        for index in reversed(selecionados):
            self.listbox_colunas.delete(index)
        self._update_preview()

    def reset_app(self):
        if self.df is not None:
            self._carregar_colunas(self.df.columns.tolist())
        self.spin_min_len.delete(0, "end")
        self.spin_min_len.insert(0, "6")
        self.delim_var.set(";")
        self.status_label.config(text="")
        self._update_preview()

    # ---------------- Data Preview ---------------- #
    def _update_preview(self):
        if self.df is None:
            return
        self.tree_preview.delete(*self.tree_preview.get_children())
        colunas = list(self.listbox_colunas.get(0, tk.END))
        if not colunas:
            return
        self.tree_preview["columns"] = colunas
        for col in colunas:
            self.tree_preview.heading(col, text=col)
        for _, row in self.df[colunas].head().iterrows():
            self.tree_preview.insert("", "end", values=list(row))

    # ---------------- Tooltip ---------------- #
    def _atualizar_tooltip(self):
        texto_base = "Data cleaning summary:"
        texto_espacos = f"\nSpaces removed: {self.total_espacos_removidos}"
        texto_tamanho = f"\nRows removed (min {self.spin_min_len.get()} chars): {self.linhas_removidas_por_tamanho}"
        texto_duplicatas = f"\nDuplicates removed: {self.total_duplicatas_removidas}"
        self.tooltip.texto = texto_base + texto_espacos + texto_tamanho + texto_duplicatas

    # ---------------- Generate TXT ---------------- #
    def gerar_txt(self):
        if self.df is None:
            messagebox.showwarning("Warning", "No file loaded.")
            return

        colunas_selecionadas = list(self.listbox_colunas.get(0, tk.END))
        if not colunas_selecionadas:
            messagebox.showwarning("Warning", "Select at least one column.")
            return

        try:
            min_len = int(self.spin_min_len.get())
            if min_len < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Enter a valid integer for minimum characters.")
            return

        primeira_col = colunas_selecionadas[0]
        df_filtrado, self.total_espacos_removidos = limpar_espacos_em_colunas(
            self.df[colunas_selecionadas].copy(), colunas_selecionadas
        )
        df_filtrado, self.linhas_removidas_por_tamanho = filtrar_primeira_coluna_por_tamanho(
            df_filtrado, primeira_col, min_len=min_len
        )
        df_filtrado, self.total_duplicatas_removidas = remover_duplicatas(df_filtrado, primeira_col)
        self._atualizar_tooltip()

        caminho_save = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("TXT files", "*.txt")],
            title="Save TXT file"
        )
        if not caminho_save:
            return

        try:
            df_filtrado.to_csv(caminho_save, sep=self.delim_var.get(), index=False, encoding='utf-8-sig')
            messagebox.showinfo(
                "Success",
                f"File saved at:\n{caminho_save}\n"
                f"Rows removed due to length: {self.linhas_removidas_por_tamanho}\n"
                f"Duplicates removed: {self.total_duplicatas_removidas}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedApp(root)
    root.mainloop()