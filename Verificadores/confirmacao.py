from colorama import Fore, Style, init

init(autoreset=True)

def confirmacao():
    """
    Traz um input para confirmar a volta do usuário ao menu

    Args:
        None

    Returns:
        None
    """
    input(Fore.WHITE + Style.BRIGHT + "\nPressione Enter para voltar ao menu...")