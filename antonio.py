#crea una funcion que reciba lea enteros por teclado y devuelva su suma

def suma():
    num1 = int(input("Ingrese un numero: "))
    num2 = int(input("Ingrese otro numero: "))
    suma = num1 + num2
    return suma

#crea una funcion que reciba un numero y devuelva su factorial

def factorial():
    for n in range(1, 21):
        result = 1
        for i in range(1, n+1):
            result *= i
        print(f"El factorial de {n} es: {result}")

#crea la funcion main que ejecute las funciones anteriores
def main():
    print("Su suma es: ",suma())
    factorial()

if __name__ == "__main__":
    main()