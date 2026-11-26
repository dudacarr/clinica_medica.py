import sqlite3
from datetime import datetime
from filas import GerenciadorFilas

PREFIXOS = {
    "Cardiologia": "CAR",
    "Pediatria": "PED",
    "Clínico Geral": "CLI",
    "Psiquiatria": "PSI",
    "Ginecologia": "GIN",
}

class BancoDados:
        
    def __init__(self):
        self.conexao = sqlite3.connect("clinica.db")
        self.conexao.row_factory = sqlite3.Row
        self.cursor = self.conexao.cursor()    
        self.gerenciador = GerenciadorFilas()
        
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

    def gerar_senha(self, especialidade, prioridade):
        """Ex.: CAR-N001 (normal) ou CAR-P001 (prioritário)."""
        prefixo = PREFIXOS.get(especialidade, "GER")
        letra = "P" if prioridade == "Prioritário" else "N"

        self.cursor.execute("""
            SELECT COUNT(*) FROM pacientes
            WHERE especialidade = ? AND prioridade = ?
        """, (especialidade, prioridade))
        numero = self.cursor.fetchone()[0] + 1

        return f"{prefixo}-{letra}{numero:03d}" 
        
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

        paciente = self.buscar_paciente(senha)

        if paciente is None:
            return False

        especialidade = paciente["especialidade"]
        categoria = paciente["prioridade"]

        if self.gerenciador.proximo_paciente(especialidade) != senha:
            return False

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

        if self.cursor.rowcount > 0:

            self.gerenciador.retirar_paciente(
                especialidade,
                categoria
            )

            return True

        return False
    
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
    
    def listar_historico(self):

        self.cursor.execute("""
            SELECT *
            FROM pacientes
            WHERE status = 'Finalizado'
            ORDER BY data_finalizacao DESC
        """)

        return self.cursor.fetchall()
    
    def contar_pacientes(self, especialidade):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM pacientes
            WHERE status = 'Aguardando'
            AND especialidade = ?
        """, (especialidade,))

        resultado = self.cursor.fetchone()

        return resultado[0]

    def consultar_posicao(self, senha):

        self.cursor.execute("""
            SELECT especialidade, data_cadastro
            FROM pacientes
            WHERE senha = ?
            AND status = 'Aguardando'
        """, (senha,))

        paciente = self.cursor.fetchone()

        if paciente is None:
            return None

        especialidade, data_cadastro = paciente

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM pacientes
            WHERE especialidade = ?
            AND status = 'Aguardando'
            AND data_cadastro <= ?
        """, (especialidade, data_cadastro))

        return self.cursor.fetchone()[0]
    
    def calcular_tempo_espera(self, senha):

        posicao = self.consultar_posicao(senha)

        if posicao is None:
            return None

        tempo = (posicao - 1) * 30

        return tempo
    
    def buscar_paciente(self, senha):

        self.cursor.execute("""
            SELECT *
            FROM pacientes
            WHERE senha = ?
        """, (senha,))

        return self.cursor.fetchone()
    
    def proximo_paciente(self, especialidade):

        self.carregar_filas(especialidade)

        senha = self.gerenciador.proximo_paciente(especialidade)

        if senha is None:
            return None

        return self.buscar_paciente(senha)  
    
    def paciente_em_atendimento(self, especialidade):

        self.cursor.execute("""
            SELECT * FROM pacientes
            WHERE especialidade = ?
            AND status = 'Em atendimento'
            ORDER BY data_chamada DESC, id DESC
            LIMIT 1
        """, (especialidade,))

        return self.cursor.fetchone()
            
    def carregar_filas(self, especialidade):

        if especialidade not in self.gerenciador.filas:
            return

        for fila in self.gerenciador.filas[especialidade].values():
            fila.clear()

        self.cursor.execute("""
            SELECT * FROM pacientes
            WHERE especialidade = ?
            AND status = 'Aguardando'
            ORDER BY data_cadastro ASC, id ASC
        """, (especialidade,))

        for paciente in self.cursor.fetchall():

            self.gerenciador.adicionar_paciente(
                paciente["especialidade"],
                paciente["prioridade"],
                paciente["senha"]
            )
            
    def consultar_posicao(self, senha):

        paciente = self.buscar_paciente(senha)

        if paciente is None or paciente["status"] != "Aguardando":
            return None

        especialidade = paciente["especialidade"]

        self.carregar_filas(especialidade)

        return self.gerenciador.consultar_posicao(
            especialidade,
            senha
        )