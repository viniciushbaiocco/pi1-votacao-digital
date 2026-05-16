from colorama import Fore, Style
from Visual.visual import limpar_tela
from time import sleep

def validar_chave_acesso(chave_acesso):

    """
    Verifica se a chave de acesso fornecida pelo usuário segue o padrão esperado:
    dois primeiros caracteres são letras e os quatro últimos são números, totalizando 6 dígitos.

    Args:
        chave_acesso (str): A chave de acesso a ser validada.

    Returns:
        bool: True se a chave de acesso estiver na formatação adequada, False caso contrário.
              Em caso de formatação incorreta, mensagens de erro detalhadas são impressas no console.
    """

    # Verifica se a chave de acesso possui 6 dígitos
    if len(chave_acesso) != 7:
        print(Fore.RED + Style.BRIGHT + "\nChave de Acesso INVÁLIDA")
        print(Fore.YELLOW+ Style.BRIGHT + "Chave de Acesso deve conter 7 dígitos")
        print(Fore.YELLOW + Style.BRIGHT + "Não utilize espaços ou pontuações")
        sleep(1.5)
        limpar_tela()
        return False

    # Verifica se os dois primeiros caracteres são letras
    if not chave_acesso[0:3].isalpha():
        print(Fore.RED + Style.BRIGHT + "\nChave de Acesso INVÁLIDA")
        print(Fore.YELLOW + Style.BRIGHT + "Os três primeiros dígitos devem ser LETRAS")
        sleep(1.5)
        limpar_tela()
        return False

    # Verifica se os quatro últimos caracteres são números
    if not chave_acesso[3:7].isdigit():
        print(Fore.RED + Style.BRIGHT + "\nChave de Acesso INVÁLIDA")
        print(Fore.YELLOW + Style.BRIGHT + "Os quatro últimos dígitos devem ser NÚMEROS")
        sleep(1.5)
        limpar_tela()
        return False

    return True
