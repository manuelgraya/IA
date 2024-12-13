from tictactoeAlum import *

LIMITE = 3

def PSEUDOminimax(nodo):
    mejorJugada = -1
    puntos = -2
    for jugada in jugadas:
        if esValida(nodo, jugada):
            intento = aplicaJugada(nodo, jugada, 1)
            util = utilidad(intento)
            if util > puntos:
                puntos = util
                mejorJugada = jugada
    nodo = aplicaJugada(nodo, mejorJugada, 1)
    return nodo


def jugadaAdversario(nodo):
    valida = False
    jugada = None
    while not valida:
        fila = int(input("Fila: "))
        col = int(input("Col: "))
        jugada = Jugada(fila, col)
        valida = esValida(nodo, jugada)
        if not valida:
            print("\n Intenta otra posicion del tablero \n")
    nodo = aplicaJugada(nodo, jugada, -1)
    return nodo


def minimax(nodo):
    jugador = 1
    mejorJugada = jugadas[0]
    max_puntos = -10000
    for jugada in jugadas:
        if esValida(nodo, jugada):
            intento = aplicaJugada(nodo, jugada, jugador)
            max_actual = valorMin(intento)
            if max_actual > max_puntos:
                max_puntos = max_actual
                mejorJugada = jugada
    nodo = aplicaJugada(nodo, mejorJugada, jugador)
    return nodo


def valorMin(nodo):
    if terminal(nodo):
        return utilidad(nodo)
    else:
        valor_min = float('inf')
        jugador = -1
        for jugada in jugadas:
            if esValida(nodo, jugada):
                valor_min = min(valor_min, valorMax(aplicaJugada(nodo, jugada, jugador)))
        return valor_min


def valorMax(nodo):
    if terminal(nodo):
        return utilidad(nodo)
    else:
        valor_max = float('-inf')
        jugador = 1
        for jugada in jugadas:
            if esValida(nodo, jugada):
                valor_max = max(valor_max, valorMin(aplicaJugada(nodo, jugada, jugador)))
        return valor_max


############################################################################################################
    # PODA ALFA-BETA
############################################################################################################

def heuristica(nodo):
    tablero = nodo.tablero
    jugador = 1  # Supongamos que el jugador 1 es "❌"
    oponente = -1  # Supongamos que el jugador -1 es "⭕"
    
    def contar_lineas_abiertas(tablero, jugador):
        lineas_abiertas = 0
        
        # Comprobar filas
        for fila in tablero:
            if all(casilla != oponente for casilla in fila):
                lineas_abiertas += 1
        
        # Comprobar columnas
        for col in range(tablero.shape[1]):
            if all(tablero[fila][col] != oponente for fila in range(tablero.shape[0])):
                lineas_abiertas += 1
        
        # Comprobar diagonales
        if all(tablero[i][i] != oponente for i in range(tablero.shape[0])):
            lineas_abiertas += 1
        if all(tablero[i][tablero.shape[0] - 1 - i] != oponente for i in range(tablero.shape[0])):
            lineas_abiertas += 1
        
        return lineas_abiertas
    
    lineas_abiertas_jugador = contar_lineas_abiertas(tablero, jugador)
    lineas_abiertas_oponente = contar_lineas_abiertas(tablero, oponente)
    
    return lineas_abiertas_jugador - lineas_abiertas_oponente


def poda_ab(nodo):
    jugador = 1
    alfa = float('-inf')
    beta = float('inf')
    prof = 0
    mejorJugada = jugadas[0]
    
    for jugada in jugadas:
        if esValida(nodo, jugada):
            intento = aplicaJugada(nodo, jugada, jugador)
            v = valorMin_ab(intento, prof+1, alfa, beta)
            if v > alfa:
                alfa = v
                mejorJugada = jugada
    
    nodo = aplicaJugada(nodo, mejorJugada, jugador)
    return nodo


def valorMin_ab(nodo, prof, alfa, beta):
    if terminal(nodo):
        return utilidad(nodo)
    else:
        if prof == LIMITE:
            return heuristica(nodo)
        else:
            vmin = float('inf')
            i = 0
            while i < len(jugadas) and alfa < beta:
                jugada = jugadas[i]
                if esValida(nodo, jugada):
                    intento = aplicaJugada(nodo, jugada, -1)
                    beta = min(beta, valorMax_ab(intento, prof+1, alfa, beta))
                i += 1
            vmin = beta
        return vmin


def valorMax_ab(nodo, prof, alfa, beta):
    if terminal(nodo):
        return utilidad(nodo)
    else:
        if prof == LIMITE:
            return heuristica(nodo)
        else:
            vmax = float('-inf')
            i = 0
            while i < len(jugadas) and alfa < beta:
                jugada = jugadas[i]
                if esValida(nodo, jugada):
                    intento = aplicaJugada(nodo, jugada, 1)
                    alfa = max(alfa, valorMin_ab(intento, prof+1, alfa, beta))
                i += 1
            vmax = alfa
        return vmax
