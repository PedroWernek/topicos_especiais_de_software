"""
3. Escreva um método que retorne o maior valor entre dois números inteiros.
"""

def maior_entre(num1: int, num2: int) -> int:
    if num1 > num2:
        return num1
    elif num2 > num1:
        return num2
    else:
        return "Erro, eles são iguais"

num1, num2 = map(int, input("Digite os dois numeros para ver qual é maior: ").split())

print(f"O maior é: {maior_entre(num1, num2)}")
