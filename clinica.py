# Painel Médico

def criar_painel_medico(self):
    tk.label(self.aba_medico, text="Painel Médico", font=("Arial", 19, "bold"), bg='white', fg="#17365d").pack(pady=20)
    controles = tk.Frame(self.aba_medico, bg='white')
    controles.pack(pady=10)
    tk.label(controles, text="Especialidade:", bg='white').grid(row=0, column=0, padx=5, pady=5) 