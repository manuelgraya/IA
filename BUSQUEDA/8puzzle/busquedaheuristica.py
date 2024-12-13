from __future__ import annotations
from NPuzle_Alum import *
from dataclasses import dataclass


@dataclass
class Nodo:
    estado: tEstado
    operador: str
    costeCamino: int
    profundidad: int
    padre: Nodo
    funcion_eval: int
    modo: str = "1"
 
    def __lt__(self, other: Nodo) -> bool:
        if self.modo=="a*":
            return self.funcion_eval + self.costeCamino < other.funcion_eval +other.costeCamino
        else:
            return self.funcion_eval < other.funcion_eval

def nodoInicial_manhattan() -> Nodo:
    return Nodo(estadoInicial(), None, 0, 0, None, manhattan(estadoInicial()))

def nodoInicial_malcolocadas() -> Nodo:
    return Nodo(estadoInicial(), None, 0, 0, None, malcolocadas(estadoInicial()))

def nodoInicial_manhattan_estrella() -> Nodo:
    return Nodo(estadoInicial(), None, 0, 0, None, manhattan(estadoInicial()), "a*")


def dispCamino(nodo: Nodo) -> None:
    lista = []
    aux = nodo
    while aux.padre != None:
        lista.append((aux.estado.tablero, aux.operador))
        aux = aux.padre
    for i in lista[::-1]: # Se utiliza ::-1 para recorrer la lista en sentido inverso, desde la raíz hasta el nodo objetivo.
        print("Operador: ", operadores[i[1]], "\n", i[0])
        print()


def dispSolucion(nodo: Nodo) -> None:
    dispCamino(nodo)
    print("Profundidad: ", nodo.profundidad)
    print("Coste: ", nodo.costeCamino)


def expandir_malcolocadas(nodo: Nodo) -> list:
    nodos = [] # Lista de nodos sucesores del nodo actual (nodo)
    
    for operador in operadores.keys():
        if esValido(operador, nodo.estado):
            nuevoEstado = aplicaOperador(operador, nodo.estado)
            nuevoNodo = Nodo(nuevoEstado, operador, nodo.costeCamino + 1, nodo.profundidad + 1, nodo, malcolocadas(nuevoEstado))
            nodos.append(nuevoNodo)
        
    return nodos

def expandir_manhattan(nodo: Nodo) -> list:
    nodos = [] # Lista de nodos sucesores del nodo actual (nodo)
    
    for operador in operadores.keys():
        if esValido(operador, nodo.estado):
            nuevoEstado = aplicaOperador(operador, nodo.estado)
            nuevoNodo = Nodo(nuevoEstado, operador, nodo.costeCamino + 1, nodo.profundidad + 1, nodo, manhattan(nuevoEstado))
            nodos.append(nuevoNodo)
        
    return nodos


def malcolocadas(estado: tEstado) -> int:
    objetivo = estadoObjetivo()
    malcolocadas = 0
    for i in range(1, 9):
        fila, col = np.where(estado.tablero == i)
        fila_obj, col_obj = np.where(objetivo.tablero == i)
        if fila != fila_obj or col != col_obj:
            malcolocadas += 1

    return malcolocadas

def manhattan(estado: tEstado) -> int:
    objetivo = estadoObjetivo()
    manhattan = 0
    for i in range(1, 9):
        fila, col = np.where(estado.tablero == i)
        fila_obj, col_obj = np.where(objetivo.tablero == i)
        if fila != fila_obj or col != col_obj:
            manhattan += abs(fila - fila_obj) + abs(col - col_obj)

    return manhattan

def Voraz() -> bool:
    objetivo = False
    raiz = nodoInicial_malcolocadas()
    abiertos =  []
    cerrados = set()
    abiertos.append(raiz)

    while not objetivo and len(abiertos) > 0:
        actual = abiertos.pop(0)
        cerrados.add(actual.estado.hash())
        if testObjetivo(actual.estado):
            objetivo = True
            dispSolucion(actual)
        else:
            sucesores = expandir_malcolocadas(actual)
            for nodo in sucesores:
                if nodo.estado.hash() not in cerrados:
                    abiertos.append(nodo)
                    cerrados.add(nodo.estado.hash())
            abiertos = sorted(abiertos)

    if not objetivo:
        print("No se ha encontrado solución")
        
    return objetivo

def Voraz_manhattan() -> bool:
    objetivo = False
    raiz = nodoInicial_manhattan()
    abiertos =  []
    cerrados = set()
    abiertos.append(raiz)

    while not objetivo and len(abiertos) > 0:
        actual = abiertos.pop(0)
        cerrados.add(actual.estado.hash())
        if testObjetivo(actual.estado):
            objetivo = True
            dispSolucion(actual)
        else:
            sucesores = expandir_manhattan(actual)
            for nodo in sucesores:
                if nodo.estado.hash() not in cerrados:
                    abiertos.append(nodo)
                    cerrados.add(nodo.estado.hash())
            abiertos = sorted(abiertos)

    if not objetivo:
        print("No se ha encontrado solución")
        
    return objetivo

def a_estrella() -> bool:
    objetivo = False
    raiz = nodoInicial_manhattan_estrella()
    abiertos =  []
    cerrados = set()
    abiertos.append(raiz)

    while not objetivo and len(abiertos) > 0:
        actual = abiertos.pop(0)
        cerrados.add(actual.estado.hash())
        if testObjetivo(actual.estado):
            objetivo = True
            dispSolucion(actual)
        else:
            sucesores = expandir_manhattan(actual)
            for nodo in sucesores:
                if nodo.estado.hash() not in cerrados:
                    abiertos.append(nodo)
                    cerrados.add(nodo.estado.hash())
            abiertos = sorted(abiertos)
