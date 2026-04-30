import random

def gerar_protocolo_votacao(numero_candidato):
    """
    Gera um protocolo de votação único.

    Args:
        numero_candidato: O número do candidato para incluir no protocolo.

    Returns:
        Uma string contendo o protocolo de votação gerado.
    """

    prefixo = "V"
    ano = 26

    # Gera duas letras maiúsculas aleatórias
    letras_aleatorias = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))

    # Gera 5 dígitos aleatórios
    numeros_aleatorios = random.randint(10000, 99999)

    protocolo_votacao = prefixo + letras_aleatorias + str(ano) + str(numero_candidato) + str(numeros_aleatorios)

    return protocolo_votacao
