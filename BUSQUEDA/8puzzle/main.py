from busquedaAlum import *
from busquedaheuristica import *

# objetivo = busquedaAnchura()
# objetivo = busquedaProfundidad()
# objetivo = busquedaProfundidadLimitada(4)
# objetivo = busquedaProfundidadLimitadaIterativa()
# objetivo = busquedaAnchuraControlRepetido()
# objetivo = busquedaProfundidadControlRepetido()
objetivo = Voraz_manhattan()
if objetivo:
    print("Se ha alcanzado una solución")
else:
    print("No se ha alcanzado ninguna solución")
