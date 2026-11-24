# Painel Médico

def criar_painel_medico(self):
        tk.label(self.aba_medico, text="Painel Médico", font=("Arial", 19, "bold"), bg='white', fg="#17365d").pack(pady=20)
        controles = tk.Frame(self.aba_medico, bg='white')
        controles.pack(pady=10)
        tk.label(controles, text="Especialidade:", bg='white').grid(row=0, column=0, padx=5, pady=5) 
        seletor = ttk.Combobox(controles, textvariable=self.especialidade, values=ESPECIALIDADES, state="readonly", width=20)
        seletor.grid(row=0, column=1, padx=5)
        seletor.bind("<<ComboboxSelected>>", lambda evento: self.atualizar_medico())
        tk.Label(controles, text="Consultorio:", bg="white").grid(row=0, column=2, padx=5)
        ttk.Entry(controles, textvariable=self.consultorio, width=18).grid(row=0, column=3, padx=5)



        quadro = tk.LabelFrame(self.aba_medico, text="Proximo paciente",
                              font=("Arial", 13, "bold"), bg="#f1f5f9", padx=30, pady=25)
        quadro.pack(fill="x", padx=60, pady=30)
        self.label_senha = tk.Label(quadro, text="---", font=("Arial", 42, "bold"),
                                   fg="#2563eb", bg="#f1f5f9")
        self.label_senha.pack(pady=10)
        self.label_nome = tk.Label(quadro, text="Nenhum paciente aguardando",
                                  font=("Arial", 17), bg="#f1f5f9")
        self.label_nome.pack(pady=5)
        self.label_prioridade = tk.Label(quadro, text="", font=("Arial", 12), bg="#f1f5f9")
        self.label_prioridade.pack(pady=5)



        botoes = tk.Frame(self.aba_medico, bg="white")
        botoes.pack(pady=15)
        tk.Button(botoes, text="CHAMAR PROXIMO", command=self.chamar,
                 bg="#2563eb", fg="white", font=("Arial", 12, "bold"),
                 padx=20, pady=12).grid(row=0, column=0, padx=10)
        tk.Button(botoes, text="FINALIZAR ATENDIMENTO", command=self.finalizar,
                 bg="#16a34a", fg="white", font=("Arial", 12, "bold"),
                 padx=20, pady=12).grid(row=0, column=1, padx=10)
        self.label_status = tk.Label(self.aba_medico, text="Aguardando atendimento",
                                    bg="white", fg="#475569", font=("Arial", 11))
        self.label_status.pack(pady=10)



def atualizar_medico(self):
       if self.paciente_atual:
           return
       paciente = self.filas.proximo(self.especialidade.get())
       if paciente:
           self.label_senha.config(text=paciente["senha"])
           self.label_nome.config(text=paciente["nome"])
           self.label_prioridade.config(text=self.especialidade.get() + " | " + paciente["prioridade"])
       else:
           self.label_senha.config(text="---")
           self.label_nome.config(text="Nenhum paciente aguardando")
           self.label_prioridade.config(text="")

def chamar(self):
       if self.paciente_atual:
           messagebox.showwarning("Atencao", "Finalize o atendimento atual primeiro.")
           return
       consultorio = self.consultorio.get().strip()
       if not consultorio:
           messagebox.showwarning("Atencao", "Informe o consultorio.")
           return
       paciente = self.filas.chamar_proximo(self.especialidade.get(), consultorio)
       if paciente is None:
           messagebox.showinfo("Fila vazia", "Nao existem pacientes aguardando.")
           self.atualizar_tudo()
           return
       self.paciente_atual = paciente["id"]
       self.label_status.config(text="Paciente chamado: " + paciente["nome"] + " | " + consultorio,
                                fg="#16a34a")
       messagebox.showinfo("Paciente chamado", "Senha: " + paciente["senha"] +
                           "\nPaciente: " + paciente["nome"] + "\nConsultorio: " + consultorio)
       self.atualizar_tudo()



   def finalizar(self):
       if self.paciente_atual is None:
           messagebox.showwarning("Atencao", "Nao existe atendimento em andamento.")
           return
       if self.banco.finalizar(self.paciente_atual):
           self.paciente_atual = None
           self.label_status.config(text="Atendimento finalizado!", fg="#16a34a")
           self.atualizar_tudo()
