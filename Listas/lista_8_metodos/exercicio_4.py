"""
4. Escreva um método que retorne o maior valor entre três números inteiros.
"""

def maior_entre_vários(*args)-> int:

    maior = args[0]
    for i in range(1, len(args)):
        if args[i] > maior:
            maior = args[i]

    return maior

print(f"digite os números separados por espaço e de enter para encontrar o maior:")
print(maior_entre_vários(*map(int, input().split())))