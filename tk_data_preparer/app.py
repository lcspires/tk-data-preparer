import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from tk_data_preparer.logic import (
    limpar_espacos_em_colunas,
    remover_duplicatas,
    filtrar_primeira_coluna_por_tamanho,
)
from tk_data_preparer.tooltip import ToolTip


def tentar_leitura_csv_variavel_sep(caminho_arquivo):
    """
    Tenta ler CSV/TXT com diferentes separadores e encodings.
    Retorna um DataFrame ou levanta Exception se falhar.
    """
    sep_list = [';', ',', '\t']
    encodings = ['utf-8', 'latin1', 'cp1252']

    for sep in sep_list:
        for enc in encodings:
            try:
                return pd.read_csv(
                    caminho_arquivo,
                    sep=sep,
                    quotechar='"',
                    encoding=enc,
                    on_bad_lines='skip'
                )
            except Exception:
                continue

    raise Exception(f"Failed to load file '{caminho_arquivo}' with common encodings and separators.")


class UnifiedApp:
    def __init__(self, root):
        self.root = root
        self.df = None
        self.total_espacos_removidos = 0
        self.linhas_removidas_por_tamanho = 0
        self.total_duplicatas_removidas = 0
        self._build_ui()

    def _build_ui(self):
        self.root.title("Tk Data Preparer")
        self.root.geometry("650x550")

        btn_select = tk.Button(self.root, text="Select File", command=self.selecionar_arquivo)
        btn_select.pack(pady=10)

        frame_min_len = tk.Frame(self.root)
        frame_min_len.pack(pady=(0, 10))
        tk.Label(frame_min_len, text="Minimum digits in 1st column:").pack(side=tk.LEFT)
        self.spin_min_len = tk.Spinbox(frame_min_len, from_=1, to=100, width=5)
        self.spin_min_len.pack(side=tk.LEFT, padx=5)
        self.spin_min_len.delete(0, "end")
        self.spin_min_len.insert(0, "3")

        self.label_resultado = tk.Label(self.root, text="", wraplength=600, justify="center")
        self.label_resultado.pack(pady=(0, 5))

        self.icone_info = tk.Label(self.root, text="ℹ️", cursor="question_arrow")
        self.icone_info.pack_forget()

        texto_tooltip = (
            "Select an Excel (.xls/.xlsx), CSV, or TXT file.\n"
            "After loading, organize columns and generate the TXT file.\n"
            "Extra spaces will be removed, and rows with fewer characters than specified will be excluded."
        )
        self.tooltip = ToolTip(self.icone_info, texto_tooltip)

        self.listbox_colunas = tk.Listbox(self.root, selectmode=tk.EXTENDED, width=50, height=15)
        self.listbox_colunas.pack(pady=10)

        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack()

        tk.Button(frame_botoes, text="↑ Move Up", command=self.mover_cima).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(frame_botoes, text="↓ Move Down", command=self.mover_baixo).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(frame_botoes, text="✖ Remove Selected", command=self.remover_colunas, fg="red").grid(row=0, column=2, padx=10, pady=5)

        btn_generate = tk.Button(self.root, text="Generate TXT", command=self.gerar_txt, bg="#4CAF50", fg="white")
        btn_generate.pack(pady=20)

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Select Excel, CSV, or TXT file",
            filetypes=[("Excel files", "*.xls *.xlsx"), ("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All files", "*.*")]
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
            self.label_resultado.config(text=f"File loaded: {caminho_arquivo}")
            self._carregar_colunas(self.df.columns.tolist())
            self.icone_info.pack(pady=(0, 10))
            self.total_espacos_removidos = 0
            self.linhas_removidas_por_tamanho = 0
            self.total_duplicatas_removidas = 0
            self._atualizar_tooltip()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def _carregar_colunas(self, colunas):
        self.listbox_colunas.delete(0, tk.END)
        for col in colunas:
            self.listbox_colunas.insert(tk.END, col)

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

    def remover_colunas(self):
        selecionados = self.listbox_colunas.curselection()
        for index in reversed(selecionados):
            self.listbox_colunas.delete(index)

    def _atualizar_tooltip(self):
        texto_base = "Data cleaning summary:"
        texto_espacos = f"\nSpaces removed: {self.total_espacos_removidos}"
        texto_tamanho = f"\nRows removed (min {self.spin_min_len.get()} chars): {self.linhas_removidas_por_tamanho}"
        texto_duplicatas = f"\nDuplicates removed: {self.total_duplicatas_removidas}"
        self.tooltip.texto = texto_base + texto_espacos + texto_tamanho + texto_duplicatas

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
            messagebox.showwarning("Warning", "Enter a valid integer for minimum length.")
            return

        primeira_col = colunas_selecionadas[0]

        # Clean whitespace
        df_filtrado, self.total_espacos_removidos = limpar_espacos_em_colunas(
            self.df[colunas_selecionadas].copy()
        )

        # Filter rows by first column length
        df_filtrado, self.linhas_removidas_por_tamanho = filtrar_primeira_coluna_por_tamanho(
            df_filtrado, primeira_col, min_len=min_len
        )

        # Remove duplicates
        df_filtrado, self.total_duplicatas_removidas = remover_duplicatas(
            df_filtrado, primeira_col
        )

        self._atualizar_tooltip()

        caminho_save = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("TXT file", "*.txt")],
            title="Save TXT file"
        )
        if not caminho_save:
            return

        try:
            df_filtrado.to_csv(caminho_save, sep=';', index=False, encoding='utf-8-sig')
            messagebox.showinfo(
                "Success",
                f"File saved:\n{caminho_save}\n"
                f"Rows removed by length: {self.linhas_removidas_por_tamanho}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedApp(root)
    root.mainloop()
