from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def validacao_palavra_chave(palavra):
    """
    Valida a palavra-chave de backup do eleitor.

    Deve conter apenas letras A-Z (sem acentos), 4 caracteres.
    A restrição de A-Z é exigida pela Cifra de Hill utilizada na criptografia.

    Args:
        palavra (str): Palavra-chave a ser validada.

    Returns:
        bool: True se válida, False caso contrário.
    """

    if not palavra.isalpha() or not palavra.isascii():
        console.print("\nPalavra-chave INVÁLIDA", style="bold red")
        console.print("\nA palavra-chave deve conter apenas letras sem acentos (A-Z)", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    if len(palavra) != 4:
        console.print("\nPalavra-chave INVÁLIDA", style="bold red")
        console.print("\nA palavra-chave deve ter exatamente 4 letras", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    return True
