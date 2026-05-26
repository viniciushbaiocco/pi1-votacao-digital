from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def validacao_de_cpf(cpf_digitado_usuario):
    """
    Valida matematicamente um CPF verificando seus dois dígitos verificadores.
    Args:
        cpf_digitado_usuario (str): O CPF a ser validado, com ou sem formatação.
    Returns:
        bool: True se o CPF for válido, False caso contrário.
    """
    # Limpando
    cpf_limpo = cpf_digitado_usuario.replace(".", "").replace("-", "").replace(" ", "")

    # Letras
    if not cpf_limpo.isdigit():
        console.print("\nCPF inválido! O CPF deve conter apenas números.", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False

    digitos = [int(d) for d in cpf_limpo]

    # Tamanho
    if len(digitos) != 11:
        console.print("\nCPF inválido! O CPF deve conter 11 dígitos.", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False

    # Sequência repetida
    if cpf_limpo == cpf_limpo[0] * 11:
        console.print("\nCPF inválido! Sequência de números repetidos.", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False

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
        console.print("\nCPF inválido!", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False

    return True
