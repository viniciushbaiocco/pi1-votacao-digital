from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def validar_chave_acesso(chave_acesso):
    """
    Verifica se a chave de acesso fornecida pelo usuário segue o padrão esperado:
    tres primeiros caracteres são letras e os quatro últimos são números, totalizando 7 dígitos.

    Args:
        chave_acesso (str): A chave de acesso a ser validada.

    Returns:
        bool: True se a chave de acesso estiver na formatação adequada, False caso contrário.
              Em caso de formatação incorreta, mensagens de erro detalhadas são impressas no console.
    """

    # Verifica se a chave de acesso possui 7 dígitos
    if len(chave_acesso) != 7:
        console.print("\nChave de Acesso INVÁLIDA", style="bold red")
        console.print("Chave de Acesso deve conter 7 dígitos", style="bold yellow")
        console.print("Não utilize espaços ou pontuações", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    # Verifica se os dois primeiros caracteres são letras
    if not chave_acesso[0:3].isalpha():
        console.print("\nChave de Acesso INVÁLIDA", style="bold red")
        console.print("Os três primeiros dígitos devem ser LETRAS", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    # Verifica se os quatro últimos caracteres são números
    if not chave_acesso[3:7].isdigit():
        console.print("\nChave de Acesso INVÁLIDA", style="bold red")
        console.print("Os quatro últimos dígitos devem ser NÚMEROS", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    return True
