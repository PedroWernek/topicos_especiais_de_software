"""
1. Escreva um método que retorne o valor absoluto de um número.
"""

def val_absoluto(x: float) -> float:
    if x < 0:
        return -x
    else:
        return x

print(val_absoluto(float(input("digite o valor que deseja o absoluto: "))))
