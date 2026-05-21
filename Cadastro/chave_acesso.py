import random

def geracao_chave_acesso(nome):
    """
    Gera uma chave de acesso única combinando partes do nome do eleitor e um número aleatório.

    O formato final da chave é composto pelas duas primeiras letras do primeiro nome em maiúsculas,
    seguidas da primeira letra do primeiro sobrenome em maiúsculas e, por fim, um sufixo numérico
    aleatório de 4 dígitos.

    Args:
        nome (str): O nome completo do eleitor.

    Returns:
        str: A chave de acesso gerada com 7 caracteres (3 letras maiúsculas e 4 números).
    """

    numero = random.randint(1000, 9999)

    partes_nome = nome.split()
    primeiro_nome = partes_nome[0]
    primeiro_sobrenome = partes_nome[1]

    iniciais_nome = primeiro_nome[:2].upper()
    inicial_sobrenome = primeiro_sobrenome[0].upper()

    chave_acesso = iniciais_nome + inicial_sobrenome + str(numero)

    return chave_acesso


