from Zerezima import zerezima
from Votacao import autenticacao_mesario
from colorama import Fore, Style
from Ocorrencias import abertura_urna, geral # Import geral to generate session_id

def abrir_sistema_votacao(id_sessao):
    """
    Executa abertura do sistema

    Args:
        None # A função não recebe argumentos diretamente, mas orquestra a abertura.

    Returns:
        bool: True se a abertura foi bem-sucedida e a urna está liberada, False caso contrário.
    """

    # 2. Tentar autenticar o mesário, passando o session_id
    if not autenticacao_mesario.autenticar_mesario(id_sessao):
        print(Fore.RED + Style.BRIGHT + "\n  [ERRO] Validação falhou.")
        print(Fore.YELLOW + Style.BRIGHT + "Confirme se o eleitor possui perfil de mesário")
        return False

    # 3. Se autenticado, realizar a zerézima
    zerezima.zerezima()
    # 4. Registrar a abertura bem-sucedida nos logs
    geral.ocorrencia_abertura_urna(id_sessao)
    abertura_urna.ocorrencia_abertura_urna(id_sessao)
    return True
