# tk_data_preparer/app.py - Day 1 MVP
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from .logic import limpar_espacos_em_colunas, remover_duplicatas, filtrar_primeira_coluna_por_tamanho
from .tooltip import ToolTip

class UnifiedApp:
    def __init__(self, root):
        self.root = root
        self.df = None
        self.total_espacos_removidos = 0
        self.linhas_removidas_por_tamanho = 0
        self.total_duplicatas_removidas = 0
        self._build_ui()

    def _build_ui(self):
        self.root.title("Tk Data Preparer - MVP")
        self.root.geometry("500x500")

        tk.Button(self.root, text="Select File", command=self.selecionar_arquivo).pack(pady=10)

        self.listbox_colunas = tk.Listbox(self.root, selectmode=tk.EXTENDED, width=50, height=20)
        self.listbox_colunas.pack(pady=10)

        tk.Button(self.root, text="Generate TXT", command=self.gerar_txt, bg="#4CAF50", fg="white").pack(pady=20)

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Select Excel, CSV or TXT",
            filetypes=[("Excel files", "*.xls *.xlsx"),
                       ("CSV files", "*.csv"),
                       ("TXT files", "*.txt")]
        )
        if not caminho_arquivo:
            return

        ext = os.path.splitext(caminho_arquivo)[1].lower()
        try:
            if ext in ['.xls', '.xlsx']:
                self.df = pd.read_excel(caminho_arquivo)
            else:
                self.df = pd.read_csv(caminho_arquivo, sep=';', on_bad_lines='skip')
            self._carregar_colunas(self.df.columns.tolist())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{e}")

    def _carregar_colunas(self, colunas):
        self.listbox_colunas.delete(0, tk.END)
        for col in colunas:
            self.listbox_colunas.insert(tk.END, col)

    def gerar_txt(self):
        if self.df is None:
            messagebox.showwarning("Warning", "No file loaded.")
            return

        colunas_selecionadas = list(self.listbox_colunas.get(0, tk.END))
        if not colunas_selecionadas:
            messagebox.showwarning("Warning", "Select at least one column.")
            return

        primeira_col = colunas_selecionadas[0]

        df_filtrado, self.total_espacos_removidos = limpar_espacos_em_colunas(
            self.df[colunas_selecionadas].copy(), colunas_selecionadas
        )
        df_filtrado, self.linhas_removidas_por_tamanho = filtrar_primeira_coluna_por_tamanho(
            df_filtrado, primeira_col, min_len=1
        )
        df_filtrado, self.total_duplicatas_removidas = remover_duplicatas(df_filtrado, primeira_col)

        caminho_save = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("TXT file", "*.txt")])
        if not caminho_save:
            return

        try:
            df_filtrado.to_csv(caminho_save, sep=';', index=False, encoding='utf-8-sig')
            messagebox.showinfo("Success", f"File saved at:\n{caminho_save}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedApp(root)
    root.mainloop()
