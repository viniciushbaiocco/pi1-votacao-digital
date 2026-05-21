from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

LETRAS_VALIDAS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áàãâéêíóôõúüçÁÀÃÂÉÊÍÓÔÕÚÜÇ-'"

def validacao_partido(partido):
    """
    Valida o nome de um partido político.

    O nome deve conter apenas letras, espaços e acentuação válida,
    com no mínimo 3 caracteres.

    Args:
        partido (str): O nome do partido a ser validado.

    Returns:
        bool: True se o nome for válido, False caso contrário.
    """

    if len(partido.strip()) < 3:
        console.print("\nNome do partido INVÁLIDO", style="bold red")
        console.print("Nome do partido deve ter no mínimo 3 caracteres", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    for caractere in partido:
        if caractere not in LETRAS_VALIDAS:
            console.print("\nNome do partido INVÁLIDO", style="bold red")
            console.print("Nome do partido deve conter apenas letras e espaços", style="bold yellow")
            sleep(1.5)
            limpar_tela()
            return False

    return True
