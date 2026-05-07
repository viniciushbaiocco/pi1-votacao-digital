from colorama import Fore, Style, init

init(autoreset=True)

def validar_cpf_voto(cpf):
    """
    Verifica se o CPF fornecido possui exatamente 4 dígitos,

    Args:
        cpf (str): A string contendo os quatro primeiros dígitos do CPF a ser validado.

    Returns:
        bool: True se o CPF tiver 4 dígitos, indicando um formato válido para votação.
              False caso contrário, e uma mensagem de erro é impressa.

    """

    cpf_arrumado = cpf.replace(".", "").replace("-", "").replace(" ", "")
    if len(cpf_arrumado) != 4:
        print(Fore.RED + Style.BRIGHT + "CPF INVÁLIDO")
        print(Fore.YELLOW+ Style.BRIGHT + "Para a votação digite apenas os quatro primeiros dígitos do seu CPF")
        return False

    return True
