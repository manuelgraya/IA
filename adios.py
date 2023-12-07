#funcion que reciba dos enteros y compruebe que son mayores que 0
#y que el segundo es mayor que el primero
#si no se cumplen las condiciones, debe devolver False

def comprobar_enteros(a,b):
    if a>0 and b>a:
        return True
    else:
        return False
    
#funcion que reciba por teclado dos enteros y compruebe que son mayores que 0
#y que el segundo es mayor que el primero

def comprobar_enteros_teclado():
    print ("Introduce dos números enteros mayores que 0")
    a=int(input("Introduce un número: "))
    b=int(input("Introduce otro número: "))
    if a>0 and b>a:
        return True
    else:
        return False

#funcion que reciba dos enteros y imprima los primos comprendiodos entre ellos
#si no se cumplen las condiciones, debe devolver False

def es_primo(num):
    if num < 2: # los números menores que 2 no son primos
        return False
    for i in range(2, num//2 + 1):
        if num % i == 0: # si num es divisible por cualquier número entre 2 y num, no es primo
            return False
    return True

def comprobar_enteros_primos(a,b):
    if a>0 and b>a:
        for i in range (a,b+1):
            if es_primo(i): # si i es primo, imprímelo
                print (i)
        return True
    else:
        return False
    
#funcion que reciba por teclado dos enteros y imprima los primos comprendiodos entre ellos
#si no se cumplen las condiciones, debe devolver False

def comprobar_enteros_primos_teclado():
    print ("Introduce dos números enteros mayores que 0")
    a=int(input("Introduce un número: "))
    b=int(input("Introduce otro número: "))
    if a>0 and b>a:
        for i in range (a,b+1):
            if es_primo(i): # si i es primo, imprímelo
                print (i)
        return True
    else:
        return False

def main():
    while True:
        a = int(input("Introduce un número: "))
        b = int(input("Introduce otro número: "))
        resultado = comprobar_enteros_primos(a, b)
        print(resultado)
        if resultado: #si resultado es True -> sale del bucle y termina el programa
            break

    while True:
        resultado = comprobar_enteros_primos_teclado()
        print(resultado)
        if resultado: #si resultado es True -> sale del bucle y termina el programa
            break

if __name__ == "__main__":
    main()