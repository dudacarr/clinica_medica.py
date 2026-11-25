<<<<<<< HEAD
from collections import deque


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

        for especialidade in self.especialidades:
            self.filas[especialidade] = {
                "Normal": deque(),
                "Preferencial": deque()
            }
            
    def adicionar_paciente(self, especialidade, categoria, senha):

        if especialidade not in self.filas:
            return False

        if categoria not in ["Normal", "Preferencial"]:
            return False

        self.filas[especialidade][categoria].append(senha)

        return True

    def retirar_paciente(self, especialidade, categoria):

        if especialidade not in self.filas:
            return False

        if categoria not in ["Normal", "Preferencial"]:
            return False

        if not self.filas[especialidade][categoria]:
            return None

        senha = self.filas[especialidade][categoria].popleft()

        return senha

    
=======
from collections import deque


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

        for especialidade in self.especialidades:
            self.filas[especialidade] = {
                "Normal": deque(),
                "Preferencial": deque()
            }
            
    def adicionar_paciente(self, especialidade, categoria, senha):

        if especialidade not in self.filas:
            return False

        if categoria not in ["Normal", "Preferencial"]:
            return False

        self.filas[especialidade][categoria].append(senha)

        return True

    def retirar_paciente(self, especialidade, categoria):

        if especialidade not in self.filas:
            return False

        if categoria not in ["Normal", "Preferencial"]:
            return False

        if not self.filas[especialidade][categoria]:
            return None

        senha = self.filas[especialidade][categoria].popleft()

        return senha

    
>>>>>>> 8997466df5d48e84f02fa59c6c46b3db26cd229b
