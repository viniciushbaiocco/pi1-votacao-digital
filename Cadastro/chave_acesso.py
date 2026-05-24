import random
from Validadores.validacao_chave_acesso import remover_acentos

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

    # A Cifra de Hill só aceita A-Z/0-9: remove acentos e mantém apenas letras A-Z nas iniciais
    primeiro_nome_az = ''.join(c for c in remover_acentos(primeiro_nome).upper() if 'A' <= c <= 'Z')
    primeiro_sobrenome_az = ''.join(c for c in remover_acentos(primeiro_sobrenome).upper() if 'A' <= c <= 'Z')

    iniciais_nome = primeiro_nome_az[:2]
    inicial_sobrenome = primeiro_sobrenome_az[:1]

    chave_acesso = iniciais_nome + inicial_sobrenome + str(numero)

    return chave_acesso


