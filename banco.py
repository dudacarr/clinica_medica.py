import sqlite3
from datetime import datetime

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
        
    def inserir_paciente(self, nome, senha, especialidade, prioridade):

        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.cursor.execute("""
                INSERT INTO pacientes
                (nome, senha, especialidade, prioridade, data_cadastro)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, senha, especialidade, prioridade, data_cadastro))

            self.conexao.commit()

            return True

        except sqlite3.IntegrityError:
            return False
        
    def listar_pacientes(self, especialidade=None):

        if especialidade:
            self.cursor.execute("""
                SELECT * FROM pacientes
                WHERE status = 'Aguardando'
                AND especialidade = ?
            """, (especialidade,))
        else:
            self.cursor.execute("""
                SELECT * FROM pacientes
                WHERE status = 'Aguardando'
            """)

        return self.cursor.fetchall()
    
    def chamar_paciente(self, senha, consultorio):

        data_chamada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
            UPDATE pacientes
            SET status = 'Em atendimento',
                data_chamada = ?,
                consultorio = ?
            WHERE senha = ?
            AND status = 'Aguardando'
        """, (data_chamada, consultorio, senha))

        self.conexao.commit()

        return self.cursor.rowcount > 0
    
    def finalizar_atendimento(self, senha):

        data_finalizacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
            UPDATE pacientes
            SET status = 'Finalizado',
                data_finalizacao = ?
            WHERE senha = ?
            AND status = 'Em atendimento'
        """, (data_finalizacao, senha))

        self.conexao.commit()

        return self.cursor.rowcount > 0
