import tkinter as tk
from tkinter import messagebox, ttk

class SistemaMicroempreendedorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Auxiliar de Estoque - Microempreendedor")
        self.root.geometry("750x550")
        self.root.config(bg="#f4f6f9")

        # Base de dados simulada (Lista de itens: Nome, Tipo, Quantidade, Mínimo)
        self.estoque = [
            {"nome": "Tecido Algodão (Metro)", "tipo": "Matéria-Prima", "qtd": 12, "min": 15},
            {"nome": "Linha Costura Branca", "tipo": "Matéria-Prima", "qtd": 40, "min": 10},
            {"nome": "Bolsa Ecológica Pronta", "tipo": "Produto Pronto", "qtd": 8, "min": 5},
        ]

        # Título do Topo
        titulo_label = tk.Label(root, text="Gestão de Estoque e Produção para Microempreendedores", 
                                font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#333333")
        titulo_label.pack(pady=10)

        # Frame de Cadastro
        frame_cadastro = tk.LabelFrame(root, text=" Cadastro de Itens (Estoque / Matéria-Prima) ", 
                                       font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#0056b3", padx=10, pady=10)
        frame_cadastro.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_cadastro, text="Nome do Item:", bg="#f4f6f9").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_cadastro, width=25)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_cadastro, text="Tipo:", bg="#f4f6f9").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.combo_tipo = ttk.Combobox(frame_cadastro, values=["Matéria-Prima", "Produto Pronto"], width=15, state="readonly")
        self.combo_tipo.grid(row=0, column=3, padx=5, pady=5)
        self.combo_tipo.current(0)

        tk.Label(frame_cadastro, text="Quantidade:", bg="#f4f6f9").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_qtd = tk.Entry(frame_cadastro, width=10)
        self.entry_qtd.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(frame_cadastro, text="Estoque Mínimo:", bg="#f4f6f9").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.entry_min = tk.Entry(frame_cadastro, width=10)
        self.entry_min.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        btn_adicionar = tk.Button(frame_cadastro, text="Adicionar ao Estoque", bg="#28a745", fg="white", 
                                  font=("Arial", 9, "bold"), command=self.adicionar_item)
        btn_adicionar.grid(row=2, column=0, columnspan=4, pady=10)

        # Frame de Visualização / Tabela
        frame_tabela = tk.LabelFrame(root, text=" Visão Geral do Estoque e Alertas ", 
                                     font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#0056b3", padx=10, pady=10)
        frame_tabela.pack(fill="both", expand=True, padx=15, pady=5)

        # Treeview (Tabela)
        columns = ("Nome", "Tipo", "Quantidade", "Mínimo", "Status Alerta")
        self.tree = ttk.Treeview(frame_tabela, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Botões de Ação Inferior
        frame_botoes = tk.Frame(root, bg="#f4f6f9")
        frame_botoes.pack(fill="x", padx=15, pady=10)

        btn_atualizar = tk.Button(frame_botoes, text="Atualizar Lista", bg="#007bff", fg="white", 
                                  font=("Arial", 9, "bold"), command=self.atualizar_tabela)
        btn_atualizar.pack(side="left", padx=5)

        btn_excluir = tk.Button(frame_botoes, text="Remover Selecionado", bg="#dc3545", fg="white", 
                                font=("Arial", 9, "bold"), command=self.remover_item)
        btn_excluir.pack(side="left", padx=5)

        # Popular dados iniciais
        self.atualizar_tabela()

    def adicionar_item(self):
        nome = self.entry_nome.get().strip()
        tipo = self.combo_tipo.get()
        qtd_str = self.entry_qtd.get().strip()
        min_str = self.entry_min.get().strip()

        if not nome or not qtd_str or not min_str:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return

        try:
            qtd = int(qtd_str)
            min_val = int(min_str)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e Mínimo devem ser números inteiros!")
            return

        self.estoque.append({"nome": nome, "tipo": tipo, "qtd": qtd, "min": min_val})
        self.atualizar_tabela()

        # Limpar campos
        self.entry_nome.delete(0, tk.END)
        self.entry_qtd.delete(0, tk.END)
        self.entry_min.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")

    def atualizar_tabela(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.estoque:
            # Lógica do alerta automático exigido no objetivo
            if item["qtd"] <= item["min"]:
                status = "⚠️ ESTOQUE BAIXO!"
            else:
                status = "Normal"

            self.tree.insert("", "end", values=(item["nome"], item["tipo"], item["qtd"], item["min"], status))

    def remover_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return
        
        for item in selected_item:
            index = self.tree.index(item)
            del self.estoque[index]
        
        self.atualizar_tabela()
        messagebox.showinfo("Sucesso", "Item removido com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaMicroempreendedorApp(root)
    root.mainloop()