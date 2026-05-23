from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def validar_cpf_voto(cpf):
    """
    Verifica se o CPF fornecido possui exatamente 4 dígitos,

    Args:
        cpf (str): A string contendo os quatro primeiros dígitos do CPF a ser validado.

    Returns:
        bool: True se o CPF tiver 4 dígitos e apenas números, indicando um formato válido para votação.
              False caso contrário, e uma mensagem de erro é impressa.

    """

    cpf_arrumado = cpf.replace(".", "").replace("-", "").replace(" ", "")


    if len(cpf_arrumado) != 4:
        console.print("\nCPF INVÁLIDO", style="bold red")
        console.print("\nPara a votação digite apenas os quatro primeiros dígitos do seu CPF", style="bold yellow")
        sleep(1.5)
        limpar_tela()
        return False

    for caractere in cpf_arrumado:
        if not caractere.isdigit():
            console.print("\nCPF INVÁLIDO", style="bold red")
            console.print("\nO CPF deve conter apenas números. Não digite letras ou símbolos.", style="bold yellow")
            sleep(1.5)
            limpar_tela()
            return False

    return True

