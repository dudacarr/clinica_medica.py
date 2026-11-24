import sqlite3

class BancoDados:

    def __init__(self):
        self.conexao = sqlite3.connect("clinica.db")
        self.cursor = self.conexao.cursor()
        
    def criar_tabela(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL UNIQUE,
                especialidade TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                data_cadastro TEXT NOT NULL,
                status TEXT DEFAULT 'Aguardando',
                data_chamada TEXT,
                data_finalizacao TEXT,
                consultorio TEXT
            )
        """)

        self.conexao.commit()
        