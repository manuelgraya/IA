(deftemplate aereonave

    (slot id )
    (slot compania)
    (slot aerodromo_origen)
    (slot aerodromo_destino)
    (slot velocidad_actual (type INTEGER))
    (slot peticion (allowed-values ninguna despegue aterrizaje emergencia rumbo))
    (slot estado (allowed-values enTierra ascenso crucero descenso)(default enTierra))

)

(deftemplate aerodromo

    (slot id)
    (slot ciudad)
    (slot radar (allowed-values ON OFF)(default ON))
    (slot visibilidad (type INTEGER))
    (slot viento (type INTEGER))

)

(deftemplate piloto

    (slot id_aereonave)
    (slot id_vuelo)
    (slot estado (allowed-values OK SOS ejecutando stand-by)(default stand-by))

)

(deftemplate vuelo

    (slot id)
    (slot id_aerodromo_O)
    (slot id_aerodromo_D)
    (slot distancia(type INTEGER))
    (slot velocidad_despegue(type INTEGER)(default 240))
    (slot velocidad_crucero(type INTEGER)(default 700))

)

; Despegar: se	realizará	esta	acción	cuando	una	aeronave	que	se	encuentra	en	tierra	haya	realizado	esta	
; petición	 al	 aeródromo	 de	 origen,	 el	 piloto	 de	 la	 misma	 ha	 dado	 su	 visto	 bueno (estado	OK) y	 en	 el	
; aeródromo	de	origen	el	 radar	 funciona	correctamente,	el	 radio	de	visibilidad	es	mayor	de	5	kms	y	la	
; velocidad	 del	 viento	 es	 menor	 de	 75km/h. Además,	 debe	 existir	 un	 vuelo	 con	 el	 origen	 y	 destino	
; especificados	 en	 la	 aeronave. La	 autorización	 de	 despegue	 implica	 que	 el	 piloto	 pasa	 al	 estado	 de	
; Ejecutando (esta	acción)		y	la	aeronave	al	estado	Ascenso. La	velocidad	actual	debe	tomar	el	valor	de	la	
; velocidad	de	despegue establecida	para	este	vuelo.		Se	actualiza	la	petición	de	la	aeronave	a	Ninguna.

(defrule Despegar

    ?aereonave <-(aereonave (id ?id) (compania ?compania)(peticion despegue) (estado enTierra))
    ?piloto <-(piloto (id_aereonave ?id)( id_vuelo ?id_vuelo)(estado OK))
    (aerodromo (id ?id_aerodromo_O)(radar ON) (visibilidad ?v) (viento ?w))
    (aerodromo (id ?id_aerodromo_D))
    (vuelo (id ?id_vuelo)(id_aerodromo_O ?id_aerodromo_O) (id_aerodromo_D ?id_aerodromo_D)(velocidad_despegue ?v_despegue))
    (test (>= ?v 5))
    (test (< ?w 75))
    =>
    (modify ?aereonave (estado ascenso) (peticion ninguna)(velocidad_actual ?v_despegue))
    (modify ?piloto (estado ejecutando))
    (printout t crlf "La areonave" ?id "de la compañia" ?compania  "va a realizar la acción de despegue desde el aeródromo" ?id_aerodromo_O "con destino al aeródromo" ?id_aerodromo_D crlf)
)

; Excepción:	 Cuando el piloto	asociado	a	una	aeronave no	se	encuentra	en	estado	OK, para	realizar	un	
; vuelo	 de	 los	 registrados	 en	 el	 aeródromo	 de	 origen pero la	 aeronave	 se	 encuentra	 en	 petición	 de	
; Despegue. La aeronave	realiza	 una	petición de Emergencia mostrando	un	mensaje	 que	indique	este	
; estado	de	excepción.

(defrule Excepcion

    ?aereonave <- (aereonave (id ?id) (peticion despegue)(compania ?compania))
    (piloto (id_aereonave ?id)(id_vuelo ?id_vuelo)(estado ~OK))
    (vuelo (id ?id_vuelo)(id_aerodromo_O ?id_aerodromo_O) (id_aerodromo_D ?id_aerodromo_D))
    =>
    (modify ?aereonave (peticion emergencia))
    ; ATENCION El	piloto	de	la	aeronave	FX220	de	la	compañía	IB	no	se	encuentra	disponible para	iniciar	el	despegue		desde	el	aeródromo	MAD	con	destino	BCN
    (printout t crlf "ATENCION El piloto de la aeronave " ?id " de la compañia" ?compania " no se encuentra disponible para iniciar el despegue desde el aerodromo " ?id_aerodromo_O " con destino " ?id_aerodromo_D crlf)
)

; Crear	dos	funciones	en	Clips	para	calcular	el	tiempo	para	llegar	al	destino,	según	
; la	velocidad	de	crucero	y	la	distancia	en	kms.
; Una	función	ha	de	devolver	el	número	de	horas	y	la	otra	los	minutos. Por	ejemplo	una	aeronave	que	va	a	
; velocidad	de	crucero	800	km/h	tardará	en	recorrer	880	kms	1	hora	y	6	minutos.
; (Puedes	usar	las	funciones	div	y	mod si	las	necesitas)


(deffunction calcular_horas (?distancia ?velocidad)
    (div ?distancia ?velocidad)
)

(deffunction calcular_minutos (?distancia ?velocidad)
    (bind ?aux(mod ?distancia ?velocidad))
    (bind ?aux2(mod ?aux ?velocidad))
    (* ?aux2 60) ; minutos
)

; Crucero:	 	 La	velocidad	 de	 crucero	 se	alcanza	 después	 de	 que	el	 piloto	 ha	 realizado	 una	maniobra de	
; despegue,	 la	 aeronave	 se	 encuentra	 en	 el	 estado	Ascenso	 y	 pasa	 a Crucero, donde,	 a	 partir	 de	 la	
; velocidad	inicial	se	alcanza	la	altura	y	velocidad	de	crucero	establecidas	para	este	vuelo,	esta velocidad
; se	actualizará	en	esta	 regla. En	este	momento	se	informa	a	los	pasajeros	de	que	el	despegue	ha	sido	
; correcto	 y	 se	 estima	 el	 tiempo	 de	 vuelo,	 que	 se	 calcula	 con	 la	 distancia	 al	 destino	 y	 la	 velocidad	 de	
; crucero	 alcanzada.	 (Se	 ha	 de	 crear	 una	 función	 que	 devuelva	 esta	 estimación).	 	 El	 estado	 del	 piloto	
; pasará	a	stand-by.


(defrule Crucero

    ?aereonave <- (aereonave (id ?id) (estado ascenso))
    ?vuelo <- (vuelo (id ?id_vuelo)(velocidad_crucero ?v_crucero)(distancia ?d))
    =>
    (modify ?aereonave (estado crucero)(velocidad_actual ?v_crucero))
    (printout t crlf "La areonave" ?id "ha alcanzado la velocidad de crucero " ?v_crucero "km/h" crlf)
    (printout t crlf "El tiempo estimado de vuelo es de " (calcular_horas ?d ?v_crucero) "horas y" (calcular_minutos ?d ?v_crucero) " minutos" crlf)
)

