from Zerezima import zerezima
from Votacao import autenticacao_mesario

def _solicitar_credenciais_mesario() -> tuple:
    """
    Pede ao usuário credenciais pra autenticação
      - Título de eleitor
      - 4 primeiros dígitos do CPF
      - Chave de acesso
 
    Args:
        None
 
    Returns:
       Tupla (titulo, primeiros_digitos_cpf, chave_acesso), todos str.
    """
    print("\n" + "=" * 55)
    print("  ABERTURA DO SISTEMA DE VOTAÇÃO")
    print("=" * 55)
    print("  Autenticação do Mesário")
    print("-" * 55)
 
    titulo = input("  Título de eleitor : ")
    primeiros_cpf = input("  4 primeiros dígitos do CPF : ")
    chave = input("  Chave de acesso : ").upper()
 
    return titulo, primeiros_cpf, chave

def abrir_sistema_votacao():
    """
    Executa abertura do sistema

    Args:
        None
 
    Returns:
        True se a abertura foi bem-sucedida e a urna está liberada, False caso contrário.
    """
    titulo, primeiros_cpf, chave = _solicitar_credenciais_mesario()
 
    autenticado = autenticacao_mesario.autenticar_mesario(titulo, primeiros_cpf, chave)
 
    if not autenticado:
        print("\n  [ERRO] Validação falhou.")
        print("  Verifique o título, os dígitos do CPF e a chave de acesso,")
        print("  ou confirme se o eleitor possui perfil de mesário.")
        return False
 
    zerezima.zerezima()
     return True