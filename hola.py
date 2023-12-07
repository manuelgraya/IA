import random

# Función para imprimir el tablero
def imprimir_tablero(tablero):
    for fila in tablero:
        print("|".join(fila))
        print("-----")

# Función para verificar si hay un ganador
def verificar_ganador(tablero, jugador):
    # Verificar filas
    for fila in tablero:
        if all(casilla == jugador for casilla in fila):
            return True

    # Verificar columnas
    for columna in range(3):
        if all(tablero[fila][columna] == jugador for fila in range(3)):
            return True

    # Verificar diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == jugador:
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] == jugador:
        return True

    return False

# Función para jugar al Tictactoe

def jugar_tictactoe():
    tablero = [[" " for _ in range(3)] for _ in range(3)]
    jugador_actual = "X"

    while True:
        imprimir_tablero(tablero)

        if jugador_actual == "X":
            fila = int(input("Ingrese el número de fila (0-2): "))
            columna = int(input("Ingrese el número de columna (0-2): "))

            if tablero[fila][columna] != " ":
                print("Esa casilla ya está ocupada. Intente de nuevo.")
                continue

            tablero[fila][columna] = jugador_actual
        else:
            fila = random.randint(0, 2)
            columna = random.randint(0, 2)

            if tablero[fila][columna] != " ":
                continue

            tablero[fila][columna] = jugador_actual

        if verificar_ganador(tablero, jugador_actual):
            imprimir_tablero(tablero)
            if jugador_actual == "X":
                print("¡Has ganado!")
            else:
                print("¡La IA ha ganado!")
            break

        if all(casilla != " " for fila in tablero for casilla in fila):
            imprimir_tablero(tablero)
            print("¡Empate!")
            break

        jugador_actual = "O" if jugador_actual == "X" else "X"

# Iniciar el juego
jugar_tictactoe()
