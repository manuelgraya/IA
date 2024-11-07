(defglobal ?*ANNIO* = 2024)
(defglobal ?*LIMITE_BANCO* = 1000)

(deftemplate usuario
    (slot dni)
    (slot pin)
    (slot dinero (default 0))
)

(deftemplate tarjeta
    (slot pin)
    (slot dni)
    (slot nIntentos (default 3))
    (slot limiteDinero (default 1000))
    (slot añoExp (default 2028))
    (slot validada (allowed-values Si No) (default No))
)

(deftemplate cuenta
    (slot dni)
    (slot saldo)
    (slot estado (allowed-values enPantalla dineroEntregado inicial superaLimite sinSaldo) (default inicial))

)

(deffacts iniciales

(tarjeta (dni 123456) (pin 1212) (nIntentos 3) (limiteDinero 500) (añoExp 2026))
(tarjeta (dni 456456) (pin 4545) (nIntentos 3) (limiteDinero 500) (añoExp 2026))
(tarjeta (dni 000111) (pin 0011) (nIntentos 0) (limiteDinero 500) (añoExp 2026))
(cuenta (dni 123456) (saldo 5000))
(cuenta (dni 456456) (saldo 33))
(cuenta (dni 000111) (saldo 30000))

)

(defrule Supera_Intentos
    (declare(salience 100)) ;PRIORIDAD MAXIMA
    ?f1 <- (usuario (dni ?dni))
    (tarjeta (dni ?dni) (nIntentos 0))
    =>
    (printout t crlf "Superado el numero de intentos")
    (retract ?f1) ;echamos al usuario
)

(deffunction decrementar(?intentos)
    (- ?intentos 1)
    ;se devuelve la ultima operacion que devuelva valor
)

(defrule Pin_Invalido
    ;RESTRICCIONES DE CAMPO
    (usuario (dni ?dni) (pin ?pin1))
    ?tarjeta <- (tarjeta (dni ?dni) (pin ?pin2) (nIntentos ?int))
    (test (neq ?pin1 ?pin2))
    =>
    (bind ?aux (decrementar ?int));se pasa por copia
    (modify ?tarjeta (nIntentos ?aux))
)

(defrule validar_tarjeta
    (usuario (dni ?dni) (pin ?pin))
    ?tarjeta <-(tarjeta (dni ?dni) (pin ?pin) (validada No)(nIntentos ?intentos)(añoExp ?anyo))
    (test (>= ?anyo ?*ANNIO*))
    (test (> ?intentos 0))
    =>
    (modify ?tarjeta (validada Si))    
)

(defrule muestra_saldo

    (usuario (dni ?dni))
    (tarjeta (dni ?dni) (validada Si))
    ?cuenta <- (cuenta (dni ?dni) (saldo ?saldo))
    =>
    (printout t crlf "Saldo: " ?saldo)
    (modify ?cuenta (estado enPantalla))
)

(defrule saldo_insuficiente

    (usuario (dni ?dni)(dinero ?dinero))
    (tarjeta (dni ?dni)(validada Si))
    (cuenta (dni ?dni)(estado enPantalla)(saldo ?saldo))
    (test (< ?saldo ?dinero))
    (test (>= ?saldo 0))
    =>
    (printout t crlf "Saldo insuficiente para esta operación")

)

(defrule saldo_negativo

    ?user <- (usuario (dni ?dni)(pin ?pin))
    (tarjeta (dni ?dni) (pin ?pin) (validada Si))
    (cuenta (dni ?dni)(estado enPantalla)(saldo ?saldo))
    (test (< ?saldo 0))
    =>
    (printout t crlf "Saldo negativo")
    (retract ?user)

)

(defrule comprobar_limte1

    ?user <- (usuario (dni ?dni)(dinero ?dinero))
    (tarjeta (dni ?dni)(validada Si))
    (test (> ?dinero ?*LIMITE_BANCO*))
    =>
    (printout t crlf "Se ha superado el limite de dinero")    
    (retract ?user)
)

(defrule comprobar_limte1

    ?user <- (usuario (dni ?dni)(dinero ?dinero))
    (tarjeta (dni ?dni)(validada Si)(limiteDinero ?limite))
    (test (> ?dinero ?limite))
    =>
    (printout t crlf "Se ha superado el limite de dinero")    
    (retract ?user)
)

(deffunction resta(?saldo ?dinero)
    (- ?saldo ?dinero)
)

(defrule entrega_dinero

    ?user <- (usuario (dni ?dni)(dinero ?dinero))
    (tarjeta (dni ?dni)(validada Si)(limiteDinero ?limite))
    ?cuenta <- (cuenta (dni ?dni) (saldo ?saldo))
    (test (>= ?saldo ?dinero))
    =>
    (bind ?aux (resta ?saldo ?dinero))
    (printout t crlf "Dinero entregado, saldo actual: " ?aux)  
    (printout t crlf " ")
    (modify ?cuenta (saldo ?aux)(estado dineroEntregado))  
    (retract ?user)

)
