import numpy as np 
from dataclasses import dataclass 
from copy import deepcopy 


@dataclass
class Nodo:
    tablero: np.array
    vAlturas: np.array
    ultima_ficha = None
    fila: int
    col: int
    

    def __init__(self, tablero):
        self.tablero = tablero
        self.vAlturas = np.array([5, 5, 5, 5, 5, 5, 5])
        self.ultima_ficha = None
        self.col = None

    def __str__(self):
        visual = {-1: "🟡", 1: "🔴", 0.0: " "}
        string = ""
        for i in range(self.tablero.shape[0]):
            for j in range(self.tablero.shape[1]):
                if i==0 and j==0:
                    string+="|"
                if self.tablero[i, j] == 0:
                    string += "    |"
                else:
                    string += f" {visual[self.tablero[i, j]]} |"
            if  i < self.tablero.shape[0]-1:
                string += f"\n ----+----+----+----+----+----+----\n|"
            else:
                
                string += f"\n ----+----+----+----+----+----+----\n"
        return f"{string}"

def NodoInicial():
    tablero = np.zeros((6,7))
    return Nodo(tablero)

def NodoInicial_Poda():
    tablero = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, 0, 1],
        [1, 1, -1, 0, -1, -1, 1],
        [-1, 1, -1, -1, 1, 1, -1],
        [-1, -1, 1, 1, -1, 1, 1],
        [1, -1, -1, -1, 1, 1, -1]
    ])
    return Nodo(tablero)


def aplicaJugada(actual: Nodo, jugador: int) -> Nodo:
    nuevo = deepcopy(actual)
    nuevo.tablero[nuevo.vAlturas[nuevo.col], nuevo.col] = jugador
    nuevo.ultima_ficha = [nuevo.vAlturas[nuevo.col], nuevo.col]
    nuevo.vAlturas[nuevo.col] -= 1
    return nuevo

def esValida(actual: Nodo) -> bool:
    if actual.col == None:
        return False
    elif actual.vAlturas[actual.col] >= 0:
        return True
    else:
        return False

def terminal(actual: Nodo) -> bool:
    if np.count_nonzero(actual.tablero) == 42:
        return True
    elif utilidad(actual) != 0:
        return True
    else:
        return False

def utilidad(nodo: Nodo) -> int:
    copia = deepcopy(nodo)
    jugador = copia.tablero[copia.ultima_ficha[0], copia.ultima_ficha[1]]
    x = copia.ultima_ficha[0]
    y = copia.ultima_ficha[1]
    
    # Comprobamos si hay 4 en raya en horizontal
    contador = 0
    for i in range (7):
        if copia.tablero[x, i] == jugador:
            contador += 1
            if contador == 4:
                return jugador*100
        else:
            contador = 0
    
    # Comprobamos si hay 4 en raya en vertical
    contador = 0
    for i in range (6):
        if copia.tablero[i, y] == jugador:
            contador += 1
            if contador == 4:
                return jugador*100
        else:
            contador = 0
                
    # Comprobamos si hay 4 en raya en diagonal
    contador = 0
    diagonal_izquierda = calcular_diagonal_izquierda(copia.ultima_ficha)
    diagonal_derecha = calcular_diagonal_derecha(copia.ultima_ficha)
    
    # Comprobamos la diagonal izquierda
    rango = 7-diagonal_izquierda[0]
    if diagonal_izquierda[0] < 4 and diagonal_izquierda[1]< 5:
        for i in range(rango):
            if copia.tablero[diagonal_izquierda[0]+i, diagonal_izquierda[1]+i] == jugador:
                contador += 1
                if contador == 4:
                    return jugador*100
            else:
                contador = 0
    
    # Comprobamos la diagonal derecha
    # valores_no_permitidos = [(6,7),(5,7),(4,7),(0,0),(0,1),(0,2)]
    # if diagonal_derecha not in valores_no_permitidos:
    if diagonal_izquierda[0] < 4 and diagonal_izquierda[1]>2:
        for i in range(rango):
            if copia.tablero[diagonal_derecha[0]+i, diagonal_derecha[1]-i] == jugador:
                contador += 1
                if contador == 4:
                    return jugador*100
            else:
                contador = 0

    return 0


def calcular_diagonal_izquierda(diagonal: tuple) -> tuple:
    x, y = diagonal
    if x == 0 or y == 0:
        return diagonal
    else:
        calcular_diagonal_izquierda((x-1, y-1))


def calcular_diagonal_derecha(diagonal: tuple) -> tuple:
    x, y = diagonal
    if x == 0 or y == 7:
        return diagonal
    else:
        calcular_diagonal_derecha((x-1, y+1))


def heuristica(nodo: Nodo) -> int:
    raise NotImplementedError
