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


def nodoInicial() -> Nodo:
    return Nodo(estadoInicial(), None, 0, 0, None)


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


def expandir(nodo: Nodo) -> list:
    nodos = [] # Lista de nodos sucesores del nodo actual (nodo)
    
    for operador in operadores.keys():
        if esValido(operador, nodo.estado):
            nuevoEstado = aplicaOperador(operador, nodo.estado)
            nuevoNodo = Nodo(nuevoEstado, operador, nodo.costeCamino + 1, nodo.profundidad + 1, nodo)
            nodos.append(nuevoNodo)
        
    return nodos


def busquedaAnchura() -> bool:
    objetivo = False
    raiz = nodoInicial() 
    abiertos = []
    sucesores = []
    abiertos.append(raiz)

    # while not objetivo and len(abiertos)>0:
    #     actual = abiertos.pop(0)
    #     sucesores=expandir(actual)
    #     for nodo in sucesores:
    #         if testObjetivo(nodo.estado):     ESTA ES MI VERSION 1ST TIME
    #             objetivo = True
    #             dispSolucion(nodo)
    #             break
    #         abiertos.append(nodo)

    while not objetivo and len(abiertos)>0:
        actual=abiertos[0]
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if not objetivo:
            sucesores = expandir(actual)
            abiertos = abiertos + sucesores
            # abiertos = sucesores + abiertos

    if objetivo:
        dispSolucion(actual)  # Se muestra la solución
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo

def busquedaProfundidad() -> bool:
    objetivo = False
    raiz = nodoInicial() 
    abiertos = []
    sucesores = []
    abiertos.append(raiz)

    while not objetivo and len(abiertos)>0:
        actual=abiertos[0]
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if not objetivo:
            sucesores = expandir(actual)
            # abiertos = abiertos + sucesores
            abiertos = sucesores + abiertos

    if objetivo:
        dispSolucion(actual)  # Se muestra la solución
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo

def busquedaProfundidadLimitada(Limite) -> bool:
    objetivo = False
    raiz = nodoInicial() 
    abiertos = []
    sucesores = []
    abiertos.append(raiz)
    while not objetivo and len(abiertos)>0:
        actual=abiertos[0]
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if not objetivo and Limite > actual.profundidad:
            sucesores = expandir(actual)
            abiertos = sucesores + abiertos            
        
        

    if objetivo:
        dispSolucion(actual)  # Se muestra la solución
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo

def busquedaProfundidadLimitadaIterativa() -> bool:
    

    for i in range(1, 100):
        if busquedaProfundidadLimitada(i):
            return True
    return False

def repetidos(nodo: Nodo, cerrados: list) -> bool:
    for i in cerrados:
        if iguales(nodo.estado, i):
            return True
    return False

def busquedaAnchuraControlRepetido() -> bool:
    objetivo = False
    raiz = nodoInicial() 
    abiertos = []
    sucesores = []
    cerrados = []
    abiertos.append(raiz)

    while not objetivo and len(abiertos)>0:
        actual=abiertos[0]
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if not objetivo and not repetidos(actual, cerrados):
            sucesores = expandir(actual)
            abiertos = abiertos + sucesores
            cerrados.append(actual.estado)

    if objetivo:
        dispSolucion(actual)  # Se muestra la solución
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo

def busquedaProfundidadControlRepetido() -> bool:
    objetivo = False
    raiz = nodoInicial() 
    abiertos = []
    sucesores = []
    cerrados = []
    abiertos.append(raiz)

    while not objetivo and len(abiertos)>0:
        actual=abiertos[0]
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if not objetivo and not repetidos(actual, cerrados):
            sucesores = expandir(actual)
            abiertos = abiertos + sucesores
            cerrados.append(actual.estado)
    if objetivo:
        dispSolucion(actual)  # Se muestra la solución
    elif not objetivo:
        print("No se ha encontrado solución")