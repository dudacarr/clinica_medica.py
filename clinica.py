# Painel Médico

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import random
from datetime import datetime
from banco import BancoDados

ESPECIALIDADES = [
    "Cardiologia",
    "Pediatria",
    "Clínico Geral",
    "Psiquiatria",
    "Ginecologia"
]


PRIORIDADES = [
    "Normal",
    "Prioritário"
]
class SistemaClinica:

    def __init__(self, janela):
        self.janela = janela
        
        self.banco = BancoDados() #A:conectando o banco aqui
        self.banco.criar_tabela()

        self.janela.title("Sistema de Atendimento - Clínica Médica")
        self.janela.geometry("1000x650")
        self.janela.configure(bg="white")

        self.paciente_atual = None
        self.agendamento = None

        self.especialidade = tk.StringVar()
        self.consultorio = tk.StringVar()

        self.telas = ttk.Notebook(self.janela)
        self.telas.pack(fill="both", expand=True)

        self.aba_medico = tk.Frame(self.telas, bg="white")
        self.aba_espera = tk.Frame(self.telas, bg="white")
        self.aba_historico = tk.Frame(self.telas, bg="white")
        self.aba_cadastro = tk.Frame(self.telas, bg="white")

        self.telas.add(self.aba_medico, text="Painel Médico")
        self.telas.add(self.aba_espera, text="Sala de Espera")
        self.telas.add(self.aba_historico, text="Histórico")
        self.telas.add(self.aba_cadastro, text="Cadastro de Pacientes")

        self.criar_painel_medico()
        self.criar_painel_espera()
        self.criar_painel_historico()
        self.criar_painel_cadastro()

    def criar_painel_medico(self):
        tk.Label(self.aba_medico, text="Painel Médico", font=("Arial", 19, "bold"), bg='white', fg="#17365d").pack(pady=20)
        controles = tk.Frame(self.aba_medico, bg='white')
        controles.pack(pady=10)
        tk.Label(controles, text="Especialidade:", bg='white').grid(row=0, column=0, padx=5, pady=5)
        seletor = ttk.Combobox(controles, textvariable=self.especialidade, values=ESPECIALIDADES, state="readonly", width=20)
        seletor.grid(row=0, column=1, padx=5)
        seletor.bind("<<ComboboxSelected>>", lambda evento: self.atualizar_medico())
        tk.Label(controles, text="Consultorio:", bg="white").grid(row=0, column=2, padx=5)
        ttk.Entry(controles, textvariable=self.consultorio, width=18).grid(row=0, column=3, padx=5)

        quadro = tk.LabelFrame(self.aba_medico, text="Proximo paciente",
                               font=("Arial", 13, "bold"), bg="#f1f5f9", padx=30, pady=25)
        quadro.pack(fill="x", padx=60, pady=30)
        self.Label_senha = tk.Label(quadro, text="---", font=("Arial", 42, "bold"),
                                    fg="#2563eb", bg="#f1f5f9")
        self.Label_senha.pack(pady=10)
        self.Label_nome = tk.Label(quadro, text="Nenhum paciente aguardando",
                                   font=("Arial", 17), bg="#f1f5f9")
        self.Label_nome.pack(pady=5)
        self.Label_prioridade = tk.Label(quadro, text="", font=("Arial", 12), bg="#f1f5f9")
        self.Label_prioridade.pack(pady=5)

        botoes = tk.Frame(self.aba_medico, bg="white")
        botoes.pack(pady=15)
        tk.Button(botoes, text="CHAMAR PROXIMO", command=self.chamar,
                  bg="#2563eb", fg="white", font=("Arial", 12, "bold"),
                  padx=20, pady=12).grid(row=0, column=0, padx=10)
        tk.Button(botoes, text="FINALIZAR ATENDIMENTO", command=self.finalizar,
                  bg="#16a34a", fg="white", font=("Arial", 12, "bold"),
                  padx=20, pady=12).grid(row=0, column=1, padx=10)
        self.Label_status = tk.Label(self.aba_medico, text="Aguardando atendimento",
                                     bg="white", fg="#475569", font=("Arial", 11))
        self.Label_status.pack(pady=10)

    def atualizar_medico(self):
        if self.paciente_atual:
            return
        paciente = self.banco.proximo_paciente(self.especialidade.get())
        if paciente:
            self.Label_senha.config(text=paciente["senha"])
            self.Label_nome.config(text=paciente["nome"])
            self.Label_prioridade.config(text=self.especialidade.get() + " | " + paciente["prioridade"])
        else:
            self.Label_senha.config(text="---")
            self.Label_nome.config(text="Nenhum paciente aguardando")
            self.Label_prioridade.config(text="")

    def chamar(self):
        if self.paciente_atual:
            messagebox.showwarning("Atencao", "Finalize o atendimento atual primeiro.")
            return

        consultorio = self.consultorio.get().strip()

        if not consultorio:
            messagebox.showwarning("Atencao", "Informe o consultorio.")
            return

        paciente = self.banco.proximo_paciente(self.especialidade.get())

        if paciente is None:
            messagebox.showinfo("Fila vazia", "Nao existem pacientes aguardando.")
            self.atualizar_tudo()
            return

        if self.banco.chamar_paciente(paciente["senha"], consultorio):
            self.paciente_atual = paciente["senha"]

            self.Label_status.config(
                text="Paciente chamado: " + paciente["nome"] + " | " + consultorio,
                fg="#16a34a"
            )

            messagebox.showinfo(
                "Paciente chamado",
                "Senha: " + paciente["senha"] +
                "\nPaciente: " + paciente["nome"] +
                "\nConsultorio: " + consultorio
            )

            self.atualizar_tudo()

    def finalizar(self):
        if self.paciente_atual is None:
            messagebox.showwarning("Atencao", "Nao existe atendimento em andamento.")
            return
        if self.banco.finalizar_atendimento(self.paciente_atual):
            self.paciente_atual = None
            self.Label_status.config(text="Atendimento finalizado!", fg="#16a34a")
            self.atualizar_tudo()

    def criar_painel_espera(self):
        tk.Label(self.aba_espera, text="TEMPO DE ESPERA POR ESPECIALIDADE",
                 font=("Arial", 17, "bold"), bg="white", fg="#17365d").pack(pady=25)
        colunas = ("especialidade", "quantidade", "senha", "tempo")
        self.tabela = ttk.Treeview(self.aba_espera, columns=colunas, show="headings", height=10)
        titulos = {"especialidade": "Especialidade", "quantidade": "Pacientes aguardando",
                   "senha": "Proxima senha", "tempo": "Tempo estimado"}
        larguras = {"especialidade": 220, "quantidade": 180, "senha": 150, "tempo": 180}
        for coluna, titulo in titulos.items():
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(coluna, width=larguras[coluna], anchor="center")
        self.tabela.pack(fill="x", padx=35, pady=20)
        self.Label_horario = tk.Label(self.aba_espera, text="", bg="white", fg="#64748b")
        self.Label_horario.pack(pady=10)
        tk.Button(self.aba_espera, text="ATUALIZAR", command=self.atualizar_tudo,
                  bg="#2563eb", fg="white", font=("Arial", 11, "bold"),
                  padx=20, pady=10).pack(pady=10)

    def atualizar_espera(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for especialidade in ESPECIALIDADES:
            quantidade = self.banco.contar_pacientes(especialidade)
            paciente = self.banco.proximo_paciente(especialidade)

            senha = paciente["senha"] if paciente else "---"
            tempo = quantidade * 30

            self.tabela.insert("", "end", values=(
                especialidade,
                quantidade,
                senha,
                str(tempo) + " minutos"
            ))

        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.Label_horario.config(text="Ultima atualizacao: " + horario)

    def criar_painel_historico(self):
        tk.Label(self.aba_historico, text="HISTORICO DE ATENDIMENTOS",
                 font=("Arial", 17, "bold"), bg="white", fg="#17365d").pack(pady=20)
        colunas = ("senha", "nome", "especialidade", "status", "consultorio")
        self.tabela_historico = ttk.Treeview(self.aba_historico, columns=colunas, show="headings")
        titulos = {"senha": "Senha", "nome": "Paciente", "especialidade": "Especialidade",
                   "status": "Status", "consultorio": "Consultorio"}
        for coluna, titulo in titulos.items():
            self.tabela_historico.heading(coluna, text=titulo)
        self.tabela_historico.pack(fill="both", expand=True, padx=25, pady=20)

    def atualizar_historico(self):
        for item in self.tabela_historico.get_children():
            self.tabela_historico.delete(item)
        for paciente in self.banco.listar_historico():
            valores = (paciente["senha"], paciente["nome"], paciente["especialidade"],
                       paciente["status"], paciente["consultorio"] or "---")
            self.tabela_historico.insert("", "end", values=valores)

    def atualizar_tudo(self):
        self.atualizar_medico()
        self.atualizar_espera()
        self.atualizar_historico()

    def agendar_atualizacao(self):
        self.atualizar_tudo()
        self.agendamento = self.janela.after(10000, self.agendar_atualizacao)

    def fechar(self):
        if self.agendamento:
            self.janela.after_cancel(self.agendamento)
        self.banco.fechar()
        self.janela.destroy()
        
    def criar_painel_cadastro(self):

        tk.Label(
            self.aba_cadastro,
            text="CADASTRO DE PACIENTE",
            font=("Arial", 19, "bold"),
            bg="white",
            fg="#17365d"
        ).pack(pady=25)

        formulario = tk.Frame(self.aba_cadastro, bg="white")
        formulario.pack(pady=20)

        # Nome
        tk.Label(formulario, text="Nome do paciente:",
                bg="white", font=("Arial", 12)).grid(
                    row=0, column=0, sticky="w", pady=12
                )

        self.nome_cadastro = tk.Entry(formulario, width=35,
                                    font=("Arial", 12))
        self.nome_cadastro.grid(row=0, column=1, padx=10)

        # Especialidade
        tk.Label(formulario, text="Especialidade:",
                bg="white", font=("Arial", 12)).grid(
                    row=1, column=0, sticky="w", pady=12
                )

        self.especialidade_cadastro = ttk.Combobox(
            formulario,
            values=ESPECIALIDADES,
            state="readonly",
            width=32
        )
        self.especialidade_cadastro.grid(row=1, column=1, padx=10)

        # Prioridade
        tk.Label(formulario, text="Prioridade:",
                bg="white", font=("Arial", 12)).grid(
                    row=2, column=0, sticky="w", pady=12
                )

        self.prioridade_cadastro = ttk.Combobox(
            formulario,
            values=PRIORIDADES,
            state="readonly",
            width=32
        )
        self.prioridade_cadastro.grid(row=2, column=1, padx=10)

        # Botão
        tk.Button(
            self.aba_cadastro,
            text="CADASTRAR PACIENTE",
            command=self.salvar_cadastro,
            bg="#2563eb",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12
        ).pack(pady=25)

    def salvar_cadastro(self):

        nome = self.nome_cadastro.get()
        especialidade = self.especialidade_cadastro.get()
        prioridade = self.prioridade_cadastro.get()

        senha = self.banco.gerar_senha(especialidade, prioridade)

        resultado = self.cadastrar_paciente(
            nome,
            senha,
            especialidade,
            prioridade
        )

        if resultado:
            messagebox.showinfo(
                "Cadastro realizado",
                f"Paciente cadastrado com sucesso!\nSenha: {senha}"
            )

            self.nome_cadastro.delete(0, tk.END)
            self.especialidade_cadastro.set("")
            self.prioridade_cadastro.set("")
            
            self.atualizar_tudo()

        else:
            messagebox.showerror(
                "Erro",
                "Não foi possível cadastrar. Verifique os dados."
            )

    def cadastrar_paciente(self, nome, senha, especialidade, prioridade):

        if not nome.strip() or especialidade not in ESPECIALIDADES or prioridade not in PRIORIDADES:
            return False

        return self.banco.inserir_paciente(
            nome.strip(),
            senha,
            especialidade,
            prioridade
        )

if __name__ == "__main__":
    janela = tk.Tk()
    sistema = SistemaClinica(janela)
    janela.mainloop()