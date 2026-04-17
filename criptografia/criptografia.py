ALFABETO = "ZABCDEFGHIJKLMNOPQRSTUVWXY0123456789" #Alfabeto com Z=0 e A=1
MODULO = 36

MATRIZ_CHAVE = [
    [5, 8],
    [17, 3]
]
'''
Matriz-chave 2x2 = [5 8; 17 3]; de acordo com requisito ✅
det = 23; é invertível ✅
'''

# Funções matemáticas

def mdc(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a
''' 
Calcula o MDC dde a e b

Args:
    a (int): Primeiro numero
    b (int): segundo numero

Returns:
    int: o MDC em a
''' 

def inverso_modular(a: int, m: int) -> int:
    if mdc(a, m) != 1:
        raise ValueError(
            f"Inverso modular de {a} em mod {m} não existe. "
            f"mdc({a}, {m}) = {mdc(a, m)} ≠ 1."
        )

    # Algoritmo estendido de Euclides
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1
"""
Calcula o inverso modular de 'a' no módulo 'm' com 
Euclides ou famoso pmodulo do SciLab

Args:
    a (int): Valor do inverso modular que é calculado.
    m (int): O módulo.

Returns:
        int: O inverso modular de a em mod m.

Raises:
    ValueError: Se o inverso modular não existir (mdc(a, m) != 1).
    """


def inversa_matriz_2x2(matriz: list, mod: int) -> list:
    """
    Calcula a matriz inversa de uma matriz 2x2 em aritmética modular.

    A fórmula para inversa de [[a,b],[c,d]] é:
    (1/det) * [[d, -b], [-c, a]]  (mod 'mod')

    Args:
        matriz (list): Matriz 2x2 representada como lista de listas [[a,b],[c,d]].
        mod (int): O módulo para a aritmética.

    Returns:
        list: A matriz inversa 2x2 em mod 'mod'.

    Raises:
        ValueError: Se o determinante não for invertível no módulo dado.
    """
    a, b = matriz[0][0], matriz[0][1]
    c, d = matriz[1][0], matriz[1][1]

    det = (a * d - b * c) % mod
    inv_det = inverso_modular(det, mod)

    inversa = [
        [(inv_det * d) % mod,  (inv_det * (-b)) % mod],
        [(inv_det * (-c)) % mod, (inv_det * a) % mod]
    ]
    return inversa