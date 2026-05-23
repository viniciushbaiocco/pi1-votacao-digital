from rich.console import Console
from time import sleep
from Visual.visual import limpar_tela

console = Console(highlight=False)

def validacao_sigla_partido(sigla_partido):
    """
    Valida a sigla de um partido político.

    A sigla deve conter apenas letras e ter um comprimento entre 2 e 6 caracteres.
    Em caso de validação falha, exibe uma mensagem de erro no console e limpa a tela.

    Args:
        sigla_partido (str): A sigla do partido a ser validada.

    Returns:
        bool: True se a sigla for válida, False caso contrário.
    """

    if not sigla_partido.isalpha():
        console.print("\nSigla INVÁLIDA", style="bold red")
        console.print("\nSigla deve conter apenas letras", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    if len(sigla_partido) < 2 or len(sigla_partido) > 6:
        console.print("\nSigla INVÁLIDA", style="bold red")
        console.print("\nSigla deve conter de 2 a 6 letras", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    return True

def validacao_numero_votacao(numero_votacao):

    """
    Valida o número de votação de um candidato.

    O número de votação deve conter apenas dígitos e ter exatamente dois dígitos.
    Em caso de validação falha, exibe uma mensagem de erro no console e limpa a tela.

    Args:
        numero_votacao (str): O número de votação a ser validado.

    Returns:
        bool: True se o número de votação for válido, False caso contrário.
    """

    if not numero_votacao.isdigit():
        console.print("\nNúmero de Votação INVÁLIDO", style="bold red")
        console.print("\nNúmero de Votação deve conter apenas dígitos", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    if len(numero_votacao) < 2 or len(str(numero_votacao)) > 2:
        console.print("\nNúmero de Votação INVÁLIDO", style="bold red")
        console.print("\nNúmero de Votação deve conter apenas dois dígitos", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    return True



