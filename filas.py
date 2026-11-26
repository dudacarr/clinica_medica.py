from collections import deque
from copy import deepcopy

class GerenciadorFilas:

    def __init__(self):
        self.especialidades = [
            "Cardiologia",
            "Pediatria",
            "Clínico Geral",
            "Psiquiatria",
            "Ginecologia"
        ]

        self.filas = {}
        self.contadores = {}
        for especialidade in self.especialidades:
            self.filas[especialidade] = {
                "Normal": deque(),
                "Prioritário": deque()
            }

            self.contadores[especialidade] = 0

        for especialidade in self.especialidades:
            self.filas[especialidade] = {
                "Normal": deque(),
                "Prioritário": deque()
            }
            
    def adicionar_paciente(self, especialidade, categoria, senha):

        if especialidade not in self.filas:
            return False

        if categoria not in ["Normal", "Prioritário"]:
            return False

        self.filas[especialidade][categoria].append(senha)

        return True

    def retirar_paciente(self, especialidade, categoria):

        if especialidade not in self.filas:
            return False

        if categoria not in ["Normal", "Prioritário"]:
            return False

        if not self.filas[especialidade][categoria]:
            return None

        senha = self.filas[especialidade][categoria].popleft()

        if categoria == "Prioritário":
            self.contadores[especialidade] += 1
        else:
            self.contadores[especialidade] = 0

        return senha
    
    def proxima_categoria(self, especialidade):

        if especialidade not in self.filas:
            return None

        normal = self.filas[especialidade]["Normal"]
        prioritario = self.filas[especialidade]["Prioritário"]

        if prioritario and (self.contadores[especialidade] < 2 or not normal):
            return "Prioritário"

        if normal:
            return "Normal"

        return None
    
    def proximo_paciente(self, especialidade):

        categoria = self.proxima_categoria(especialidade)

        if categoria is None:
            return None

        return self.filas[especialidade][categoria][0]
    
    def consultar_posicao(self, especialidade, senha):

        simulacao = deepcopy(self)
        posicao = 1

        while True:

            categoria = simulacao.proxima_categoria(especialidade)

            if categoria is None:
                return None

            proxima_senha = simulacao.retirar_paciente(
                especialidade,
                categoria
            )

            if proxima_senha == senha:
                return posicao

            posicao += 1

    
