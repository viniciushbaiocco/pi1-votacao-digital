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
        bool: Retorna True se o CPF for válido, False caso contrário.
    """

    #Verificação do (1º dígito verificador)
    arrumando = cpf_digitado_usuario.replace(".", "").replace("-", "").replace(" ", "")

    #Verificação de tamanho do CPF
    if len(arrumando) != 11:
        console.print("CPF inválido! O CPF deve conter 11 dígitos", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False
    
    #Verificação se têm números repitidos
    if arrumando == arrumando [0] * len(arrumando):
        console.print("CPF inválido! Sequência de números repetidos.", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False
    
    #Verificação se tem letras
    try:
        separado = [int(i) for i in arrumando]
    except ValueError:
        console.print("CPF inválido! O CPF deve conter apenas números.", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False
    lista_1_DV = [10, 9, 8, 7, 6, 5, 4, 3, 2]

    soma_1_DV = 0
    for i in range (9):
        soma_1_DV = soma_1_DV + (separado [i] * lista_1_DV [i])
    resto_1_DV = soma_1_DV % 11
    if resto_1_DV < 2:
        digito_1_DV = 0
    else:
        digito_1_DV = 11 - resto_1_DV
    simples_1_DV = separado[:9]
    nova_lista_1_DV = simples_1_DV + [digito_1_DV]

    #Verificação do (2º dígito verificador)
    lista_2_DV = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_2_DV = 0
    for i in range(10):
            soma_2_DV = soma_2_DV + nova_lista_1_DV[i] * lista_2_DV[i]
    resto_2_DV = soma_2_DV % 11
    digito_2_DV = 0 if resto_2_DV < 2 else 11 - resto_2_DV
    if digito_1_DV != separado[9] or digito_2_DV != separado[10]:
        console.print("CPF inválido!", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False

    return True