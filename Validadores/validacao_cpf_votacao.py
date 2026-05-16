from colorama import Fore, Style
from Visual.visual import limpar_tela
from time import sleep

def validar_cpf_voto(cpf):
    """
    Verifica se o CPF fornecido possui exatamente 4 dígitos,

    Args:
        cpf (str): A string contendo os quatro primeiros dígitos do CPF a ser validado.

    Returns:
        bool: True se o CPF tiver 4 dígitos e apenas números, indicando um formato válido para votação.
              False caso contrário, e uma mensagem de erro é impressa.

    """

    cpf_arrumado = cpf.replace(".", "").replace("-", "").replace(" ", "")

    if len(cpf_arrumado) != 4:
        print(Fore.RED + Style.BRIGHT + "\nCPF INVÁLIDO")
        print(Fore.YELLOW+ Style.BRIGHT + "Para a votação digite apenas os quatro primeiros dígitos do seu CPF")
        sleep(1.5)
        limpar_tela()
        return False


    # Verfica se o cpf só possui letras
    for i in cpf_arrumado:
        if i.isalpha():
            print(Fore.RED + Style.BRIGHT + "\nCPF INVÁLIDO")
            print(Fore.YELLOW + Style.BRIGHT + "Não digite letras no CPF")
            sleep(1.5)
            limpar_tela()
            return False

    return True
