from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
import numpy as np

visual = {1: "❌", -1: "⭕", 0.0: " "}


@dataclass
class Nodo:
    tablero: np.array # Matriz 3x3 con los valores de las casillas
    vacias: int
    N: int

    def __init__(self, tablero, vacias, N):
        if tablero.shape != (3, 3):
            raise ValueError("El tablero debe ser una matriz 3x3")
        self.tablero = tablero # Matriz 3x3 con los valores de las casillas
        self.vacias = vacias
        self.N = N

    def __str__(self):
        string = f"{' ----+----+----'}\n|"
        for i in range(self.tablero.shape[0]):
            for j in range(self.tablero.shape[1]):
                if self.tablero[i, j] == 0:
                    string += "    |"
                else:
                    string += f" {visual[self.tablero[i, j]]} |"
            if i == 2 and j == 2:
                string += f"\n ----+----+----\n"
            else:
                string += f"\n ----+----+----\n|"
        return f"{string}"


@dataclass
class Jugada:
    x: int
    y: int
    
    def __str__(self):
        return f"\nFila: ({self.x}, Col: {self.y})"


######
# Se crean todas las posibles jugadas para el for de rango (for jugada in jugadas)
jugadas = []
for i in range(0, 3):
    for j in range(0, 3):
        jugadas.append(Jugada(i, j))
######

    #  Funciones complementarias
    # * crearNodo
    # * nodoInicial
    # * opuesto



def crearNodo(tablero):
    return Nodo(tablero)


def nodoInicial():
    tablero_inicial = np.zeros((3, 3)) 
    return Nodo(tablero_inicial, tablero_inicial.shape[0]*tablero_inicial.shape[1], tablero_inicial.shape[0])


def opuesto(jugador):
    return jugador * -1


""" Funciones Búsqueda MiniMax
    * aplicaJugada
    * esValida
    * terminal
    * utilidad
"""


def aplicaJugada(actual: Nodo, jugada: Jugada, jugador: int) -> Nodo:
    """Realiza una copia del nodo recibido como parámetro y aplica la jugada indicada,
    modificando para ello los atributos necesarios. Para esto, se tiene en cuenta qué
    jugador realiza la jugada.

    Args:
        actual (Nodo)
        jugada (Jugada)
        jugador (int)

    Raises:
        NotImplementedError: Mientras que no termine de implementar esta función, puede mantener
        esta excepción.

    Returns:
        Nodo: Contiene la información del nuevo estado del juego.
    
    """
    nuevo_tablero = deepcopy(actual.tablero)
    nuevo_tablero[jugada.x][jugada.y] = jugador
    nuevo_vacias = actual.vacias - 1
    nuevo_N = actual.N
    return Nodo(nuevo_tablero, nuevo_vacias, nuevo_N)



def esValida(actual: Nodo, jugada: Jugada) -> bool:
    """Comprueba si dada una Jugada, es posible aplicarla o no.

    Args:
        actual (Nodo)
        jugada (Jugada)

    Raises:
        NotImplementedError: Mientras que no termine de implementar esta función, puede mantener
        esta excepción.

    Returns:
        bool: Devuelve True en caso de que pueda realizarse la Jugada, False en caso contrario
    """
    if actual.tablero[jugada.x][jugada.y] == 0:
        return True
    else:
        return False
    raise NotImplementedError

def terminal(actual: Nodo) -> bool:
    """Comprueba si el juego se ha acabado, ya sea porque alguno de los jugadores ha ganado o bien
    porque no sea posible realizar ningún movimiento más.

    Args:
        actual (Nodo)

    Raises:
        NotImplementedError: Mientras que no termine de implementar esta función, puede mantener
        esta excepción.

    Returns:
        bool: Devuelve True en caso de Terminal, False en caso contrario
    """
    # Comprobamos si hay un ganador
    for i in range(actual.N):
        for j in range (actual.N):
            if actual.tablero[i][j] == 0:
                return False
    return True
    ###                                 Importante:
    #   Si considera más sencillo trabajar con una representación en vector en lugar de matriz puede
    #   hacer uso de la función reshape o la función flatten que contiene la biblioteca numpy. 
    #   Puede comprobar un ejemplo si ejecuta este código mediante python tictactoeAlum.py
    ###

def utilidad(nodo: Nodo) -> int:
    """La función de utilidad, también llamada objetivo, asigna un valor numérico al nodo recibido como parámetro.
    Por ejemplo, en un juego de 'Suma cero', se puede establecer que devuelve -100, 0, 100 en función de qué jugador
    gana o bien si hay un empate.

    Args:
        nodo (Nodo)

    Raises:
        NotImplementedError: Mientras que no termine de implementar esta función, puede mantener
        esta excepción.

    Returns:
        int: Valor de utilidad
    """

    # Comprobamos si hay un ganador
    for i in range(nodo.N):
        if nodo.tablero[i][0] == nodo.tablero[i][1] == nodo.tablero[i][2] != 0:
            return nodo.tablero[i][0]*100
        if nodo.tablero[0][i] == nodo.tablero[1][i] == nodo.tablero[2][i] != 0:
            return nodo.tablero[0][i]*100
    if nodo.tablero[0][0] == nodo.tablero[1][1] == nodo.tablero[2][2] != 0:
        return nodo.tablero[0][0]*100
    if nodo.tablero[0][2] == nodo.tablero[1][1] == nodo.tablero[2][0] != 0:
        return nodo.tablero[0][2]*100
    return 0


if __name__ == "__main__":
    M = np.array([
        [1,2],
        [3,4]
    ])
    print(M)
    M_vector = M.reshape(4)
    print(M_vector)
    M_vector = M.flatten()
    print(M_vector)
    M_de_nuevo = M_vector.reshape(2,2)
    print(M_de_nuevo)