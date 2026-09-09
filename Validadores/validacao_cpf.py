def validacao_de_cpf(cpf_digitado_usuario):
    """
    Valida matematicamente um CPF verificando seus dois dígitos verificadores.

    A função apenas valida: não imprime nada na tela e não limpa o terminal.
    Cabe a quem chama decidir como exibir a mensagem de erro devolvida.

    Args:
        cpf_digitado_usuario (str): O CPF a ser validado, com ou sem formatação.

    Returns:
        tuple[bool, str | None]: (True, None) se o CPF for válido.
        (False, mensagem) caso contrário, onde 'mensagem' descreve o motivo da recusa.
    """
    # Limpando
    cpf_limpo = cpf_digitado_usuario.replace(".", "").replace("-", "").replace(" ", "")

    # Letras
    if not cpf_limpo.isdigit():
        return False, "O CPF deve conter apenas números."

    digitos = [int(d) for d in cpf_limpo]

    # Tamanho
    if len(digitos) != 11:
        return False, "O CPF deve conter 11 dígitos."

    # Sequência repetida
    if cpf_limpo == cpf_limpo[0] * 11:
        return False, "Sequência de números repetidos."

    # 1 dígito verificador
    pesos_1_DV = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_1_DV  = 0
    for i in range(9):
        soma_1_DV = soma_1_DV + (digitos[i] * pesos_1_DV[i])
    resto_1_DV = soma_1_DV % 11

    if resto_1_DV < 2:
        digito_1_DV = 0
    else:
        digito_1_DV = 11 - resto_1_DV

    # 2 dígito verificador
    base_2_DV  = digitos[:9] + [digito_1_DV]
    pesos_2_DV = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_2_DV  = 0
    for i in range(10):
        soma_2_DV = soma_2_DV + (base_2_DV[i] * pesos_2_DV[i])
    resto_2_DV = soma_2_DV % 11

    if resto_2_DV < 2:
        digito_2_DV = 0
    else:
        digito_2_DV = 11 - resto_2_DV

    # Comparando
    if digito_1_DV != digitos[9] or digito_2_DV != digitos[10]:
        return False, "CPF inválido."

    return True, None
