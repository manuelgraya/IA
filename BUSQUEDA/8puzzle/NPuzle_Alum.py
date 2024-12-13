import numpy as np
from dataclasses import dataclass
import copy

operadores = {"8": "ARRIBA", "2": "ABAJO", "4": "IZQUIERDA", "6": "DERECHA"}


@dataclass
class tEstado:
    tablero: np.ndarray
    fila: int
    col: int

    def __init__(self, tablero: np.ndarray):
        self.tablero = tablero # Matriz del puzle
        self.N = self.tablero.shape[0] # Número de filas
        self.fila, self.col = np.where(self.tablero == 0) # Posición del hueco en el puzle (fila, columna)s

    def __repr__(self) -> str: # Permite representar el objeto como cadena
        return f"{self.tablero}\n Fila: {self.fila}\n Col: {self.col}\n"
    
    def hash(self) -> str:
        return str(self.tablero.tobytes())


def estadoInicial() -> tEstado:
    puzle_inicial = np.array(
    [
        [1, 0, 3], 
        [8, 2, 4],
        [7, 6, 5]
    ])
    return tEstado(puzle_inicial)


def estadoObjetivo() -> tEstado:
    puzle_final = np.array(
    [
        [1, 2, 3], 
        [8, 0, 4],
        [7, 6, 5]
    ])
    return tEstado(puzle_final)


def coste(operador: str, estado: tEstado) -> int:
    return 1


def dispOperador(operador: str) -> None:
    print(f"Operador: {operadores[operador]}")


def iguales(actual: tEstado, objetivo: tEstado) -> bool:
    iguales = False
    if np.array_equal(actual.tablero, objetivo.tablero):
        iguales = True

    return iguales


def testObjetivo(actual: tEstado) -> bool:
    objetivo = estadoObjetivo()
    return iguales(actual, objetivo)


def esValido(operador: str, estado: tEstado) -> bool:
    valido = False
    match operadores[operador]:
        case "ARRIBA":
            if estado.fila > 0:
                valido = True
        case "ABAJO":
            if estado.fila < estado.N - 1:
                valido = True
        case "IZQUIERDA":
            if estado.col > 0:
                valido = True
        case "DERECHA":
            if estado.col < estado.N - 1:
                valido = True

    return valido


def aplicaOperador(operador: str, estado: tEstado) -> tEstado:
    nuevo = copy.deepcopy(estado) # Se hace la copia completa del estado anterior
    match operadores[operador]:
        case "ARRIBA":
            nuevo.tablero[nuevo.fila, nuevo.col] = nuevo.tablero[nuevo.fila - 1, nuevo.col] # Se intercambian los valores de las casillas

        # [1, 2, 3]     [1, 2, 3]
        # [0, 4, 5]  => [1, 4, 5]
        # [8, 7, 6]     [8, 7, 6]  
            
            nuevo.tablero[nuevo.fila - 1, nuevo.col] = 0 # Se actualiza la posición del hueco

        # [1, 2, 3]     [0, 2, 3]
        # [1, 4, 5]  => [1, 4, 5]
        # [8, 7, 6]     [8, 7, 6]  

            nuevo.fila -= 1 # Se actualiza la fila del hueco en el puzle

        case "ABAJO":
            nuevo.tablero[nuevo.fila, nuevo.col] = nuevo.tablero[nuevo.fila + 1, nuevo.col]
            nuevo.tablero[nuevo.fila + 1, nuevo.col] = 0
            nuevo.fila += 1

        case "IZQUIERDA":
            nuevo.tablero[nuevo.fila, nuevo.col] = nuevo.tablero[nuevo.fila, nuevo.col - 1]
            nuevo.tablero[nuevo.fila, nuevo.col - 1] = 0
            nuevo.col -= 1

        case "DERECHA":
            nuevo.tablero[nuevo.fila, nuevo.col] = nuevo.tablero[nuevo.fila, nuevo.col + 1]
            nuevo.tablero[nuevo.fila, nuevo.col + 1] = 0
            nuevo.col += 1
           
    
    return nuevo
