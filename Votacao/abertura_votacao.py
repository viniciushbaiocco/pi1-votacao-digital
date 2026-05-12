from Zerezima import zerezima
from Votacao import autenticacao_mesario
from colorama import Fore, Style
from Ocorrencias import abertura_urna

def abrir_sistema_votacao():
    """
    Executa abertura do sistema

    Args:
        None

    Returns:
        True se a abertura foi bem-sucedida e a urna está liberada, False caso contrário.
    """

    autenticado = autenticacao_mesario.autenticar_mesario()

    if not autenticado:
        print(Fore.RED + Style.BRIGHT + "\n  [ERRO] Validação falhou.")
        print(Fore.YELLOW + Style.BRIGHT + "Confirme se o eleitor possui perfil de mesário")
        return False

    zerezima.zerezima()
    abertura_urna.ocorrencia_abertura_urna()
    return True
