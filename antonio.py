#crea una funcion que reciba lea enteros por teclado y devuelva su suma

def suma():
    num1 = int(input("Ingrese un numero: "))
    num2 = int(input("Ingrese otro numero: "))
    suma = num1 + num2
    return suma

#crea una funcion que reciba un numero y devuelva su factorial

def factorial():
    num = int(input("Ingrese un numero: "))
    factorial = 1
    for i in range(1, num+1):
        factorial = factorial * i
    return factorial

#crea la funcion main que ejecute las funciones anteriores
def main():
    print("Su suma es: ", suma())
    print(factorial())

if __name__ == "__main__":
    main()