"""
2. Escreva um método que receba dois números inteiros e retorne a soma
dos números existentes entre eles.
"""

def soma_entre(num1: int, num2: int) -> int:
    return(sum(range(num1+1,num2)))

n1, n2 = map(int, input("Digite os números que você quer ver a soma entre: (separe por espaço) ").split())
print(soma_entre(n1,n2))