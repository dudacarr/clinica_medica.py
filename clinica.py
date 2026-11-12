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
