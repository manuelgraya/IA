from busquedaAlum import *

objetivo = busquedaAnchura()
# objetivo = busquedaProfundidad()
objetivo = busquedaProfundidadLimitada(3)
objetivo = busquedaProfundidadLimitadaIterativa()
objetivo = busquedaAnchuraControlRepetido()
objetivo = busquedaProfundidadControlRepetido()
if objetivo:
    print("Se ha alcanzado una solución")
else:
    print("No se ha alcanzado ninguna solución")
