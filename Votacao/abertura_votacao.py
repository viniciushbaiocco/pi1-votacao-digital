from Zerezima import zerezima
from Votacao import autenticacao_mesario


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
        print("\n  [ERRO] Validação falhou.")
        print("Confirme se o eleitor possui perfil de mesário")
        return False

    zerezima.zerezima()
    return True
