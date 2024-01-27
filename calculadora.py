import tkinter as tk
from tkinter import messagebox
import sqlite3

class CalculadoraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Simples")

        self.resultado_var = tk.StringVar()
        self.resultado_var.set("0")

        self.operador_digitado = False  # Flag para verificar se um operador foi digitado

        # Entrada para exibir o resultado
        self.entry = tk.Entry(root, textvariable=self.resultado_var, font=('Arial', 16), justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, pady=10)

        # Botões
        botoes = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C'  # Botão de apagar
        ]

        row_val = 1
        col_val = 0

        for button in botoes:
            tk.Button(root, text=button, padx=20, pady=20, font=('Arial', 14), command=lambda b=button: self.clique_botao(b)).grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        # Menu
        menu = tk.Menu(root)
        root.config(menu=menu)

        historico_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="☰", menu=historico_menu)
        historico_menu.add_command(label="Ver Histórico", command=self.ver_historico)

        # Conectar ao banco de dados SQLite
        self.conexao = sqlite3.connect('historico.db')
        self.criar_tabela_historico()

    def criar_tabela_historico(self):
        # Criar tabela de histórico se não existir
        cursor = self.conexao.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS historico (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            expressao TEXT,
                            resultado TEXT
                          )''')
        self.conexao.commit()

    def clique_botao(self, valor):
        try:
            if valor == '=':
                expressao = self.resultado_var.get()
                resultado = str(eval(expressao))
                self.resultado_var.set(resultado)

                # Salvar no histórico
                self.salvar_no_historico(expressao, resultado)

                # Resetar a flag de operador
                self.operador_digitado = False
            elif valor == 'C':
                self.resultado_var.set("0")
                self.operador_digitado = False
            else:
                current_value = self.resultado_var.get()
                if self.operador_digitado and valor in ['+', '-', '*', '/']:
                    # Substituir o operador anterior pelo novo operador
                    self.resultado_var.set(current_value[:-1] + valor)
                else:
                    if current_value == '0':
                        self.resultado_var.set(valor)
                    else:
                        self.resultado_var.set(current_value + valor)

                # Atualizar a flag de operador
                self.operador_digitado = valor in ['+', '-', '*', '/']
        except Exception as e:
            self.resultado_var.set("Erro")

    def salvar_no_historico(self, expressao, resultado):
        # Salvar no banco de dados
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO historico (expressao, resultado) VALUES (?, ?)", (expressao, resultado))
        self.conexao.commit()

    def ver_historico(self):
        # Mostrar histórico em uma nova janela
        historico_window = tk.Toplevel(self.root)
        historico_window.title("Histórico")

        # Consultar o histórico no banco de dados
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM historico")
        historico = cursor.fetchall()

        # Exibir histórico em uma lista
        lista_historico = tk.Listbox(historico_window, width=40, height=10, font=('Arial', 12))

        for item in historico:
            expressao, resultado = item[1], item[2]
            lista_historico.insert(tk.END, f"{expressao} = {resultado}")

        lista_historico.pack(padx=10, pady=10)

# Função principal
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraGUI(root)
    root.mainloop()
