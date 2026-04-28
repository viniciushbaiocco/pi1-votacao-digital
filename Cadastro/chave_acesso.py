import random

def geracao_chave_acesso(nome):

    """
    Gera uma chave de acesso única combinando partes do nome do eleitor e um número aleatório.

    Args:
        nome (str): O nome completo do eleitor.

    Returns:
        str: A chave de acesso gerada.
    """

    numero = random.randint(1000, 9999)

    partes_nome = nome.split()
    primeiro_nome = partes_nome[0]
    primeiro_sobrenome = partes_nome[1]

    iniciais_nome = primeiro_nome[:2].upper()
    inicial_sobrenome = primeiro_sobrenome[0].upper()

    chave_acesso = iniciais_nome + inicial_sobrenome + str(numero)

    print(f"Chave de acesso {chave_acesso} criada para o eleitor {nome}")
    return chave_acesso


