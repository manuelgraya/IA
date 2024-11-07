(deftemplate valvula

    (slot nombre)
    (slot estado (allowed-values abierta cerrada) (default cerrada))
    (slot presion (default 0))
    (slot T1 (default 0))
    (slot T2 (default 0))

)

(deffacts iniciales

    (valvula (nombre Entrada) (T1 101) (T2 35) (presion 1))
    (valvula (nombre Salida) (T1 101) (T2 155) (presion 5))
    (valvula (nombre Pasillo1) (T1 99) (T2 37) (estado cerrada))

)

(defrule R1

    ?v <-(valvula (estado abierta) (presion ?presion))
    (test (eq ?presion 5))
    =>
    (modify ?v (estado cerrada) (presion 0))
)

(deffunction bucle_R2(?presion ?temperatura ?devolver)

    (while (> ?temperatura 35) 
        (bind ?temperatura (- ?temperatura 5))
        (bind ?presion (+ ?presion 1))
    )

    (if (eq ?devolver presion)
    then 
        (return ?presion)
    else
        (return ?temperatura)
    )
)

(defrule R2

    ?v <-(valvula (estado cerrada) (presion ?presion)(T1 ?T1))
    (test (< ?presion 10))
    (test (> ?T1 35))
    =>
    (bind ?presion (bucle_R2 ?presion ?T1 presion))
    (bind ?T1 (bucle_R2 ?presion ?T1 temperatura))
    (modify ?v (presion ?presion) (T1 ?T1))
)