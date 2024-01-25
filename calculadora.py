def somar(a, b):
    return a + b

def subtrair(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b != 0:
        return a / b
    else:
        return "Erro: Divisão por zero!"

if __name__ == "__main__":
    print("Calculadora Simples em Python")
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))

    print(f"\nResultados:")
    print(f"Soma: {somar(num1, num2)}")
    print(f"Subtração: {subtrair(num1, num2)}")
    print(f"Multiplicação: {multiplicar(num1, num2)}")
    print(f"Divisão: {dividir(num1, num2)}")
